# -*- coding: utf-8 -*-

from django import forms


class SzukajAdres(forms.Form):
    miejscowosc = forms.CharField(label='Miejscowosc:', max_length=180)
    precyzjamiejscowosc = forms.TypedChoiceField(coerce=lambda x: x=='0',
                                                 choices=(("0",'(zawiera)'),("1",'(dosłownie)')), widget=forms.RadioSelect, required=True,initial="0")
    ulica = forms.CharField(label='Ulica:', max_length=180, required=False)
    precyzjaulica = forms.TypedChoiceField(coerce=lambda x: x == '0',
                                                 choices=(("0", '(zawiera)'), ("1", '(dosłownie)'), ("2", '(kombinuj)')),
                                                 widget=forms.RadioSelect, required=True, initial="0")
    numer = forms.CharField(label='Numer:', max_length=180)
    precyzjanumer = forms.TypedChoiceField(coerce=lambda x: x == '0',
                                           choices=(("0", '(zawiera)'), ("1", '(dosłownie)')),
                                           widget=forms.RadioSelect, required=True, initial="0")



class SzukajWNavi(forms.Form):
    nazwapracodawcy = forms.CharField(label='Nazwa pracodawcy:', max_length=180)
