from django.urls import path

from .views import (
    index,
    CarListView,
    CarDetailView,
    CarCreateView,
    CarUpdateView,
    CarDeleteView,
    DriverListView,
    DriverDetailView,
    DriverCreateView,
    ManufacturerListView,
    ManufacturerCreateView,
    ManufacturerUpdateView,
    ManufacturerDeleteView,
    LicenseUpdateView,
    DriverDeleteView, assign_or_delete,
)

urlpatterns = [
    path("", index, name="index"),
    path("manufacturers/", ManufacturerListView.as_view(), name="manufacturer-list"),
    path("manufacturers/create/", ManufacturerCreateView.as_view(), name="manufacturer-create"),
    path("manufacturers/<int:pk>/", ManufacturerUpdateView.as_view(), name="manufacturer-update"),
    path("manufacturers/<int:pk>/delete/", ManufacturerDeleteView.as_view(), name="manufacturer-delete"),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("cars/create/", CarCreateView.as_view(), name="car-create"),
    path("cars/<int:pk>/update/", CarUpdateView.as_view(), name="car-update"),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path("drivers/create/", DriverCreateView.as_view(), name="driver-create"),
    path("drivers/<int:pk>/", DriverDetailView.as_view(), name="driver-detail"),
    path("drivers/<int:pk>/delete/", DriverDeleteView.as_view(), name="driver-delete"),
    path("drivers/<int:pk>/update_license/", LicenseUpdateView.as_view(), name="license-update"),
    path("drivers/<int:pk>/assign_or_delete/", assign_or_delete, name="assign-or-delete"),
]

app_name = "taxi"
