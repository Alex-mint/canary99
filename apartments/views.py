import folium
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseNotFound, \
    HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from canary99.settings import LANGUAGES
from django.utils import timezone

from .forms import *
from .models import *
from .utils import *


PUERTO_RICO = [27.795496216638778, -15.720274834094955]

apartment = Apartment.objects.all().first()

def check_availability(form, apartment):
    reserva_day = form.cleaned_data['check_in']
    reserva_days = (form.cleaned_data['check_out'] - form.cleaned_data[
        'check_in']).days
    reserva_dates = [reserva_day]
    for day in range(reserva_days):
        reserva_day += timedelta(days=1)
        reserva_dates.append(reserva_day)
    reserva_dates = [night.strftime('%Y-%m-%d') for night in reserva_dates]
    apart = apartment.title
    apartment = Apartment.objects.filter(title__contains=apart).first()
    not_available_date = BookingDate.objects.filter(
        booking__reserva__apartment=apartment)
    not_available_date = [night.date.strftime('%Y-%m-%d') for night in
                          not_available_date]

    if set(reserva_dates).intersection(not_available_date):
        return False
    else:
        return True


def save_reserva(form, apartment, customer):
    days = (form.cleaned_data['check_out'] - form.cleaned_data[
        'check_in']).days
    if days >= 30:
        price = apartment.price.month_price
    elif days < 30 and days >= 14:
        price = apartment.price.week_price
    else:
        price = apartment.price.day_price
    Reserva.objects.create(
        apartment=apartment,
        user=customer,
        check_in=form.cleaned_data['check_in'],
        check_out=form.cleaned_data['check_out'],
        amount_nights=days,
        price_per_night=price,
        cleaning_price=apartment.cleaning_price,
        final_price=days * price + apartment.cleaning_price
    )


def save_booking(form, customer, reserva):
    booking = Booking.objects.create(
        reserva=reserva,
        user=customer,
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
        comment=form.cleaned_data['comment'],
        phone=form.cleaned_data['phone']
    )
    amount_nights = reserva.amount_nights
    night_date = reserva.check_in - timedelta(days=1)
    for night in range(amount_nights):
        night_date += timedelta(days=1)
        BookingDate.objects.create(
            booking=booking,
            date=night_date
        )


class Home(ListView):
    model = Apartment
    template_name = 'apartments/index.html'
    context_object_name = 'apartment'

    def get_context_data(self, *, object_list=None, **kwargs):
        apartment = Apartment.objects.all().first()
        folium_map = get_map(apartment)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio'
        context['imgs'] = Images.objects.all()
        context['map'] = folium_map._repr_html_()
        return context

    def get_queryset(self):
        return Apartment.objects.all().first()


def order(request):
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        booking = Booking.objects.filter(user=customer).last()
        context = {
            'booking': booking,
            'title': 'Inicio',
            'menu': menu,
        }

        return render(request, 'apartments/order.html', context=context)
    else:
        return redirect('home')


def all_orders(request):
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        bookings = Booking.objects.filter(user=customer)
        context = {
            'bookings': bookings,
            'title': 'Inicio',
            'apartment': apartment,
        }
        return render(request, 'apartments/all_orders.html', context=context)
    else:
        return redirect('home')

def staff_page(request):
    if request.user.is_staff:
        form = StaffEditForm()
        now = timezone.now()
        bookings = Booking.objects.filter(reserva__check_out__gte=now).order_by('reserva__check_in')
        context = {
            'bookings': bookings,
            'title': 'Inicio',
            'apartment': apartment,
            'form': form,
        }
        return render(request, 'apartments/staff_page.html', context=context)
    else:
        return redirect('home')


def order_cancel(request):
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        bookings = Booking.objects.get(user=customer, status='new')
        bookings.delete()
        text = PageMessage.objects.get(title='cancel')
        messages.add_message(request, messages.INFO, text.text)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return redirect('home')


def staff_order_cancel(request, reserva_id):
    if request.user.is_staff:
        booking = get_object_or_404(Booking, pk=reserva_id)
        booking.delete()
        text = PageMessage.objects.get(title='cancel')
        messages.add_message(request, messages.INFO, text.text)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return redirect('home')


def add_staff_comment(request, reserva_id):
    form = StaffEditForm()
    return render(request, 'apartments/inc/staff-comment.html', {'form': form})


def login(request):
    return render(request, 'apartments/login.html',
                  {'title': 'login', 'apartment': apartment})


def get_map(apartment):
    map = folium.Map(location=PUERTO_RICO, zoom_start=15)
    folium.Marker(
        location=[apartment.lat, apartment.lon],
        #popup=apartment.title,
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(map)
    return map


def apart_detail(request, slug):
    apartment = get_object_or_404(Apartment, slug=slug)
    folium_map = get_map(apartment)
    if request.method == 'POST':
        form = AddReservationForm(request.POST)
        if form.is_valid():
            if check_availability(form, apartment):
                if request.user.is_authenticated:
                    customer = Customer.objects.filter(
                        user=request.user).first()
                    if not customer:
                        customer = Customer.objects.create(
                            user=request.user
                        )
                    save_reserva(form, apartment, customer)
                    return redirect('checkout')
                else:
                    return redirect('login')
            else:
                check_in = form.cleaned_data['check_in'].strftime('%d.%m.%Y')
                check_out = form.cleaned_data['check_out'].strftime('%d.%m.%Y')
                text = f"De {check_in} a {check_out} no está disponible , consulte la disponibilidad."
                messages.add_message(request, messages.INFO, text)
                form = AddReservationForm()
    else:
        form = AddReservationForm()
    today = datetime.date.today()
    images = Images.objects.filter(apartment__slug=slug)
    reservas = Booking.objects.filter(reserva__apartment__slug=slug,
                                      reserva__check_out__gte=today)
    context = {
        'apartment': apartment,
        'reservas': reservas,
        'images': images,
        'title': 'Inicio',
        'form': form,
        'map': folium_map._repr_html_(),
        'language': LANGUAGES
    }

    return render(request, 'apartments/apart_detal.html', context=context)


def checkout(request):
    customer = Customer.objects.filter(user=request.user).first()
    reserva = Reserva.objects.filter(user=customer).order_by('-id').first()
    bookings = Booking.objects.filter(user=customer, status='new')
    permit = True if (len(bookings)) < 1 else False

    if request.method == 'POST':
        form = AddBookingForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                save_booking(form, customer, reserva)
                text = 'Su reserva se guardó correctamente.'
                messages.add_message(request, messages.INFO, text)
                return redirect('all_orders')
            else:
                return redirect('home')
    else:
        form = AddBookingForm()
    context = {
        'reserva': reserva,
        'title': 'Inicio',
        'apartment': apartment,
        'form': form,
        'permit': permit
    }
    return render(request, 'apartments/checkout.html', context=context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'apartments/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        apartment = Apartment.objects.all().first()
        context = super().get_context_data(**kwargs)
        context['apartment'] = apartment
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'apartments/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        apartment = Apartment.objects.all().first()
        context = super().get_context_data(**kwargs)
        context['apartment'] = apartment
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


def page_no_found(request, exception):
    return HttpResponseNotFound('Upssss....')
