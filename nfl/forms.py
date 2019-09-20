from django.forms import ModelForm, modelformset_factory
from django.db.models import Q
from nfl.models import Selection, Team, Game, get_current_datetime
from datetime import timedelta
import django.forms as forms

class SelectionForm(ModelForm):
    class Meta:
        model = Selection
        fields = ['game','prediction']

    def __init__(self, *args, **kwargs):
        #home_team = kwargs.pop('home_team')
        #away_team = kwargs.pop('away_team')
        super(SelectionForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['game'].empty_label = None
            self.fields['game'].queryset = Game.objects.filter(pk = self.instance.game.id)
            self.fields['game'].disabled = True
            self.fields['prediction'].widget = forms.RadioSelect()
            self.fields['prediction'].queryset = Team.objects.filter(
                Q(name = self.instance.game.home_team.name) | 
                Q(name = self.instance.game.away_team.name))
            #if self.instance.game.gametime + timedelta(minutes = 10) < get_current_datetime():
            #    self.fields['prediction'].disabled = True


# SelectionFormset = modelformset_factory(Selection, fields=('prediction','game'), extra=0)
SelectionFormset = modelformset_factory(Selection, form = SelectionForm, extra=0)

