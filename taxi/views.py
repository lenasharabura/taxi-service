from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import DriverCreationForm, LicenseNummerForm, CarForm, CarSearchForm, ManufacturerSearchForm
from .models import Driver, Car, Manufacturer


@login_required
def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits + 1,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    queryset = Manufacturer.objects.all()
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context['search_form'] = ManufacturerSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")

        if name:
            return self.queryset.filter(name__icontains=name)

        return self.queryset


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    template_name = "taxi/manufacturer_form.html"


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")
    template_name = "taxi/manufacturer_confirm_delete.html"


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 2
    queryset = Car.objects.all().select_related("manufacturer")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_form'] = CarSearchForm()
        return context

    def get_queryset(self):
        model = self.request.GET.get('model')

        if model:
            return self.queryset.filter(model__icontains=model)

        return self.queryset


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/car_form.html"


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/car_confirm_delete.html"


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 2


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_confirm_delete.html"


class LicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = LicenseNummerForm
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_form.html"

    def get_success_url(self):
        return reverse("taxi:driver-detail", args=(self.object.id,))


def assign_or_delete(request, pk):
    """View function for assigning or deleting a car to a driver."""
    user_id = request.user.id
    driver = Driver.objects.get(id=user_id)
    car = Car.objects.get(id=pk)
    if car in driver.cars.all():
        driver.cars.remove(car)
    else:
        driver.cars.add(car)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[user_id]))
