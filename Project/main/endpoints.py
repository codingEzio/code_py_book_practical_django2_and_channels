from rest_framework import serializers, viewsets

from . import models


class OrderLineSerializer(serializers.HyperlinkedModelSerializer):
    """
    What is a "Serializer" then?
    || It translates the Django models into JSON
    || & then the client app translates JSON into the webpage (ha).
    """

    product = serializers.StringRelatedField()

    class Meta:
        model = models.OrderLine
        fields = ("id", "order", "product", "status")
        read_only_fields = ("id", "order", "product")


class PaidOrderLineViewSet(viewsets.ModelViewSet):
    """
    What is a "ViewSet" then?
    || It is simply a type of class-based View, that does not provide
    ||  any method handlers such as .get() or .post(),
    ||  & instead provides actions such as .list() and .create().
    """

    queryset = models.OrderLine.objects \
        .filter(order__status=models.Order.PAID) \
        .order_by("-order__date_added")

    serializer_class = OrderLineSerializer
    filter_fields = ("order", "status")


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Order
        fields = (
            "shipping_name",
            "shipping_address1",
            "shipping_address2",
            "shipping_zip_code",
            "shipping_city",
            "shipping_country",
            "date_updated",
            "date_added",
        )


class PaidOrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects \
        .filter(status=models.Order.PAID) \
        .order_by("-date_added")
    serializer_class = OrderSerializer
