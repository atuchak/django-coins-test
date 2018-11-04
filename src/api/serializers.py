from decimal import Decimal

from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError

from billing.models import Account, Payment

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User models.
    """

    class Meta:
        model = UserModel
        fields = ['id', 'username']


class AccountSerializer(serializers.Serializer):
    id = serializers.CharField()
    owner = serializers.IntegerField(source='user_id')
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))

    @staticmethod
    def validate_id(value):
        """
        Check existence of Account with pk=value

        :param value: Primary key value
        :type value: str
        :return: Returns `value` if Account with pk=value does exist.
        :rtype: str
        """
        if Account.objects.filter(pk=value).count() != 0:
            msg = _('Account with given id already exists')
            raise serializers.ValidationError(msg)
        return value

    @staticmethod
    def validate_owner(value):
        if not value:
            msg = _('Owner is required field')
            raise serializers.ValidationError(msg)

        user = UserModel.objects.filter(pk=int(value)).first()
        if not user:
            msg = _('Owner with given id not found')
            raise serializers.ValidationError(msg)

        return value

    def create(self, validated_data):
        return Account.objects.create(**validated_data)


class PaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    account = serializers.CharField(source='to_account_id')
    from_account = serializers.CharField(source='from_account_id')
    direction = serializers.CharField(read_only=True)

    @staticmethod
    def validate_amount(value):
        if value < 0:
            msg = _('Amount should be positive number')
            raise serializers.ValidationError(msg)
        return value

    @staticmethod
    def validate_to_account(value):
        try:
            Account.objects.get(pk=value)
        except Account.DoesNotExist:
            msg = _('Account with given id does not exist')
            raise serializers.ValidationError(msg)
        return value

    def validate(self, attrs):
        """
        Valis

        :param attrs: Serializer fields data
        :return: Return validated fields data
        """
        from_account_id = attrs['from_account_id']
        amount = attrs['amount']
        try:
            from_account_id = Account.objects.get(pk=from_account_id)
        except Account.DoesNotExist:
            msg = _('Account with given id does not exist')
            raise serializers.ValidationError(msg)

        if from_account_id.balance - amount < 0:
            msg = _('Account balance is not enough to process payment')
            raise serializers.ValidationError(msg)

        return attrs

    def create(self, validated_data):
        """

        :param validated_data: Validated serializer data.
        :type validated_data: dict
        :return: Returns outgoing payment for created transaction.
        :rtype: billing.models.Payment
        """
        try:
            outgoing_payment, incoming_payment = Payment.create_payment(
                amount=validated_data['amount'],
                to_account_id=validated_data['to_account_id'],
                from_account_id=validated_data['from_account_id'],
            )
        except DjangoValidationError as e:
            # Propagate exc from django model save() validation
            raise ValidationError(e.error_dict)
        return outgoing_payment
