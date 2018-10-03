from .forms import PackageForm


def test_form_validation(self):
    """ Tests to see where package form validation is failing
        Currently: Assumes one package exists in db with pk=1
    """
    form = PackageForm(package_id=1)
    assert form.package_base_form.is_valid()
    assert form.categories_formset.is_valid()
    assert form.cards_formset.is_valid()
