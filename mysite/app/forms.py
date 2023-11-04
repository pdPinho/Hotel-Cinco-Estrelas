from django import forms


## Queries ##
class user_query_form(forms.Form):
    query = forms.CharField(label='Search:', max_length=100)


## Inserts ##   
class user_insert_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=20)
    phone = forms.CharField(label='Phone Number')
    address = forms.CharField(label='Address', max_length=100)
    birthdate = forms.DateField(label='Birthdate')

class review_insert_form(forms.Form):
    review = forms.CharField(widget=forms.Textarea(attrs={"rows":"3", "placeholder":"Share your experience with us..."}), label='Write your own review', max_length=500)
    rating = forms.IntegerField(widget=forms.HiddenInput())

    # THE FOLLLOWING DOES NOT WORK FOR SOME REASON????
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        print("=====================================================")
        print(rating)
        if rating is None or rating < 1 or rating > 5:
            raise forms.ValidationError("Invalid rating. Please select a rating between 1 and 5.")
        return rating



## Edits ##
class user_edit_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=20)
    phone = forms.IntegerField(label='Phone Number')
    address = forms.CharField(label='Address', max_length=100)
    birthdate = forms.DateField(label='Birthdate')


class BookingSearchForm(forms.Form):
    data_inicial = forms.DateField(label='Data Inicial')
    data_final = forms.DateField(label='Data Final')

