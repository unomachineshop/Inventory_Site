from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from inventory.models import Items, Transactions
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Q

import json
import csv

############################################################
# Name: ItemForm (Django form class)
# Desc: This form handles all inputs necessary for the
# 'Items' model. Used in conjunction with 'item_add' and
# 'item_edit' view functions.
############################################################
class ItemForm(ModelForm):
	class Meta:
		model = Items

		fields = [
				'name_text', 
				'quantity_integer',
                'link_text',
                'price_decimal',
                'location_text',
                'description_text',
                'vendor_text',
                'vendor_id_text',
                'manufacturer_text',
                'manufacturer_id_text',
		]

		labels = {
				'name_text': 'Name',
				'quantity_integer': 'Quantity',
                'link_text': 'Link',
                'price_decimal': 'Price',
                'location_text': 'Location',
                'description_text': 'Description',
                'vendor_text': 'Vendor',
                'vendor_id_text': 'Vendor ID',
                'manufacturer_text': 'Manufacturer',
                'manufacturer_id_text': 'Manufacturer ID',
		}

############################################################
# Name: item_list
# Desc: The root view. Displays all items within the system
# grouped by their physical location.
############################################################
def item_list(request, template_name='inventory/item_list.html'): 
    data = {}
    data['Sortimo 1'] = Items.objects.get_item_by_location('Box 1')
    data['Sortimo 2'] = Items.objects.get_item_by_location('Box 2')
    data['Sortimo 3'] = Items.objects.get_item_by_location('Box 3')
    data['Sortimo 4'] = Items.objects.get_item_by_location('Box 4')
    data['Sortimo 5'] = Items.objects.get_item_by_location('Box 5')
    data['Sortimo 6'] = Items.objects.get_item_by_location('Box 6')
    data['Sortimo 7'] = Items.objects.get_item_by_location('Box 7')
    data['Sortimo 8'] = Items.objects.get_item_by_location('Box 8')
    data['Sortimo 9'] = Items.objects.get_item_by_location('Box 9')
    data['Sortimo 10'] = Items.objects.get_item_by_location('Box 10')
    data['Sortimo 11'] = Items.objects.get_item_by_location('Box 11')
    data['Sortimo 12'] = Items.objects.get_item_by_location('Box 12')
    data['Sortimo 13'] = Items.objects.get_item_by_location('Box 13')
    data['Sortimo 14'] = Items.objects.get_item_by_location('Box 14')
    data['Machine Shop'] = Items.objects.get_item_by_location('Machine Shop')
    data['Room 157'] = Items.objects.get_item_by_location('Room 157')
    data['No Location'] = Items.objects.get_item_with_no_location() 

    return render(request, template_name, {'data': data } )

############################################################
# Name: item_add
# Desc: Adds a single item to the 'Items' model. Upon form
# validation also adds an entry into the 'Transactions' 
# model, indicating the "created" type.
############################################################
def item_add(request, template_name='inventory/item_form.html'):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        item = form.save()
        h = Transactions(item_object=item, username_text="unomachine", type_text="created", quantity_integer=item.quantity_integer)
        h.save()
        return redirect('item_list')
    return render(request, template_name, {'form':form})


############################################################
# Name: item_detail
# Desc: Displays a single item's associated values from 
# both the 'Items' and 'Transactions' models.
############################################################
def item_detail(request, pk, template_name='inventory/item_detail.html'):
    item = get_object_or_404(Items, pk=pk)
    transactions = Transactions.objects.filter(item_object=item)
    data = {}
    data['item'] = item
    data['transaction_list'] = transactions
    return render(request, template_name, data)


############################################################
# Name: item_edit
# Desc: Edit a single items values. If the quantity changes
# then add the appropiate entry to the 'Transactions' model.
############################################################
def item_edit(request, pk, template_name='inventory/item_form.html'):
    item = get_object_or_404(Items, pk=pk)
    old_qty = item.quantity_integer
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        # Grab new quantity
        new_qty = form.cleaned_data.get('quantity_integer') 
        # Items added
        if old_qty < new_qty:
            t = Transactions(item_object=item, username_text="unomachine", type_text="deposit", quantity_integer=new_qty)
            t.save()

        if old_qty > new_qty:
            t = Transactions(item_object=item, username_text="unomachine", type_text="withdrawal", quantity_integer=new_qty)
            t.save()

        form.save()
        return redirect('item_detail', pk)
    return render(request, template_name, {'form':form})

############################################################
# Name: item_delete
# Desc: Delete a single item from 'Items' model. This in 
# turn removes the corresponding entries tied to that 
# item from the 'Transactions' model, known as a 
# cascading delete.
############################################################
def item_delete(request, pk, template_name='inventory/item_confirm_delete.html'):
	item = get_object_or_404(Items, pk=pk)
	if request.method == 'POST':
            h = Transactions.objects.get(pk=pk)
            h.type_text = "deleted"
            h.save()
            item.delete()
            return redirect('item_list')
	return render(request, template_name, {'object':item})

############################################################
# Name: search_results
# Desc: Returns all relevant search results.
############################################################
def search_results(request, template_name="inventory/search_results.html"):
    data = {}
    query = request.POST.get('query')
    data['results'] = Items.objects.filter(name_text__icontains=query)
    
    return render(request, template_name, data )

############################################################
# Name: get_items
# Desc: 
############################################################
def get_items(request):
    if request.is_ajax():
		# Retrieve term from the search box
        q = request.GET.get('term', '')
		# Case-insensive containment search
        items = Items.objects.filter(name_text__icontains = q )[:15]

		# Collect items names and their primary keys
        results = []
        for item in items:
            item_json = {}
            item_json['label'] = item.name_text
            item_json['value'] = reverse('item_detail', kwargs={'pk': item.id} )
            print(item_json['value'])
            results.append(item_json)
        
		# Convert to JSON
        data = json.dumps(results)
    else:
        data = 'fail'
    
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

############################################################
# Name: transactions
# Desc: Returns all transactions that are NOT of type 
# "created".
############################################################
def transactions(request, template_name="inventory/transactions.html"):
	data = {}
	data = Transactions.objects.filter(~Q(type_text="created"))
	return render(request, template_name, {'data': data } )

