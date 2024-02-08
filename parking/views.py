from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .serializers import *
from datetime import datetime


# Create your views here.
class TransactionDetailView(APIView):

    def get(self, request):

        try:
            car_number = request.GET.get("car_number", None)
            transaction = Transaction.objects.get(car_number=car_number)
            transaction_serializers = TransactionDetailSerializer(transaction)
            responses = {"status": "OK", "data": transaction_serializers.data}
            return Response(responses, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            responses = {"status": "NOT OK", "message": "Transaction not found"}
            return Response(responses, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            responses = {"status": "NOT OK", "message": str(e)}
            return Response(responses, status=status.HTTP_400_BAD_REQUEST)


class TransactionEntryView(APIView):

    def post(self, request):

        try:
            data = request.data
            car_number = data['car_number']
            data['created_user'] = request.user.id
            # get data parking capacity
            capacity = Config.objects.get(config_key="CAPACITY").config_value
            # count number of cars entring
            number_of_cars_entering = Transaction.objects.filter(parking_status=Transaction.ENTRY).count()

            if int(capacity) <= number_of_cars_entering:
                #  add queuing car
                data['parking_status'] = Transaction.QUEUE
                message = "Car %s joined the queue." % car_number

            else:
                # entry car
                data['entry_date'] = datetime.now()
                data['parking_status'] = Transaction.ENTRY
                message = "Car %s entered the car park." % car_number

            serializer_transaction = TransactionSerializer(data=data)

            if serializer_transaction.is_valid(raise_exception=True):
                transaction_saved = serializer_transaction.save()

            responses = {"status": "OK", "message": message}
            return Response(responses, status=status.HTTP_200_OK)

        except Exception as e:
            responses = {"status": "NOT OK", "message": str(e)}
            return Response(responses, status=status.HTTP_400_BAD_REQUEST)


class TransactionExitView(APIView):

    def post(self, request):
        try:
            # get transaction by car number and status entry
            user_id = request.user.id
            data = request.data
            car_number = data['car_number']
            transaction = Transaction.objects.filter(car_number=car_number, parking_status=Transaction.ENTRY)

            if transaction:
                transaction.update(modified_user=user_id, exit_date=datetime.now(), parking_status=Transaction.EXIT)

                message = "Car %s exited the car park." % car_number

                # check first queuing car number
                first_queue = Transaction.objects.filter(parking_status=Transaction.QUEUE).order_by('id')

                if first_queue:
                    queue_car = Transaction.objects.filter(id=first_queue[0].id)
                    # update status queue to entry
                    queue_car.update(created_user=user_id, entry_date=datetime.now(), parking_status=Transaction.ENTRY)
                    message = message + "\n A car exited the car park.\nCar %s exited the queue and entered the car park." % queue_car[0].car_number

                responses = {"status": "OK", "message": message}
                return Response(responses, status=status.HTTP_200_OK)
            else:
                responses = {"status": "NOT OK", "message": "Transaction not found"}
                return Response(responses, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            responses = {"status": "NOT OK", "message": "Transaction not found"}
            return Response(responses, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            responses = {"status": "NOT OK", "message": str(e)}
            return Response(responses, status=status.HTTP_400_BAD_REQUEST)


class ReportingView(APIView):

    def get(self, request):

        try:
            # get data parking capacity
            capacity = Config.objects.get(config_key="CAPACITY").config_value
            # count number of cars entring
            number_of_cars_entering = Transaction.objects.filter(parking_status=Transaction.ENTRY).count()
            # count number of cars waiting
            number_of_cars_waiting = Transaction.objects.filter(parking_status=Transaction.QUEUE).count()

            data = {
                "parking_capacity": int(capacity),
                "number_of_cars_entering": number_of_cars_entering,
                "remaining_capacity": int(capacity) - number_of_cars_entering,
                "number_of_cars_waiting": number_of_cars_waiting
            }

            responses = {"status": "OK", "data": data}
            return Response(responses, status=status.HTTP_200_OK)
        except Exception as e:
            responses = {"status": "NOT OK", "message": str(e)}
            return Response(responses, status=status.HTTP_400_BAD_REQUEST)
