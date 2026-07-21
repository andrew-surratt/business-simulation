from django import forms

from business.models import Business, ExpenseSource, RevenueSource


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ("name", "location", "type", "currency")
        widgets = {
            "name": forms.TextInput(attrs={"autofocus": True}),
            "location": forms.TextInput(attrs={"autocomplete": "address-level2"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True


class SourceForm(forms.ModelForm):
    class Meta:
        fields = ("name", "amount", "frequency", "currency")
        widgets = {
            "name": forms.TextInput(attrs={"autofocus": True}),
            "amount": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["amount"].required = True

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount is not None and amount < 0:
            raise forms.ValidationError("Enter an amount of zero or more.")
        return amount


class RevenueSourceForm(SourceForm):
    class Meta(SourceForm.Meta):
        model = RevenueSource


class ExpenseSourceForm(SourceForm):
    class Meta(SourceForm.Meta):
        model = ExpenseSource
