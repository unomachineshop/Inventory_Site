from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from inventory.models import Item, History
from django.urls import reverse
from django.http import HttpResponse

import json
import csv

class ItemForm(ModelForm):
	class Meta:
		model = Item

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

def item_list(request, template_name='inventory/item_list.html'): 
    data = {}
    data['Sortimo 1'] = Item.objects.get_item_by_location('Box 1')
    data['Sortimo 2'] = Item.objects.get_item_by_location('Box 2')
    data['Sortimo 3'] = Item.objects.get_item_by_location('Box 3')
    data['Sortimo 4'] = Item.objects.get_item_by_location('Box 4')
    data['Sortimo 5'] = Item.objects.get_item_by_location('Box 5')
    data['Sortimo 6'] = Item.objects.get_item_by_location('Box 6')
    data['Sortimo 7'] = Item.objects.get_item_by_location('Box 7')
    data['Sortimo 8'] = Item.objects.get_item_by_location('Box 8')
    data['Sortimo 9'] = Item.objects.get_item_by_location('Box 9')
    data['Sortimo 10'] = Item.objects.get_item_by_location('Box 10')
    data['Sortimo 11'] = Item.objects.get_item_by_location('Box 11')
    data['Sortimo 12'] = Item.objects.get_item_by_location('Box 12')
    data['Sortimo 13'] = Item.objects.get_item_by_location('Box 13')
    data['Sortimo 14'] = Item.objects.get_item_by_location('Box 14')
    data['Machine Shop'] = Item.objects.get_item_by_location('Machine Shop')
    data['Room 157'] = Item.objects.get_item_by_location('Room 157')
    data['No Location'] = Item.objects.get_item_with_no_location() 

    return render(request, template_name, {'data': data } )

def item_create(request, template_name='inventory/item_form.html'):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        item = form.save()
        h = History(item_object=item, username_text="unomachine", type_text="created", quantity_integer=item.quantity_integer)
        h.save()
        return redirect('item_list')
    return render(request, template_name, {'form':form})

def item_detail(request, pk, template_name='inventory/item_detail.html'):
    item = get_object_or_404(Item, pk=pk)
    history = History.objects.filter(item_object=item)
    data = {}
    data['item'] = item
    data['history_list'] = history
    return render(request, template_name, data)

def item_update(request, pk, template_name='inventory/item_form.html'):
    item = get_object_or_404(Item, pk=pk)
    old_qty = item.quantity_integer
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        # Grab new quantity
        new_qty = form.cleaned_data.get('quantity_integer') 
        # Items added
        if old_qty < new_qty:
            h = History(item_object=item, username_text="unomachine", type_text="deposit", quantity_integer=new_qty)
            h.save()

        if old_qty > new_qty:
            h = History(item_object=item, username_text="unomachine", type_text="withdrawal", quantity_integer=new_qty)
            h.save()

        form.save()
        return redirect('item_detail', pk)
    return render(request, template_name, {'form':form})

def item_delete(request, pk, template_name='inventory/item_confirm_delete.html'):
	item = get_object_or_404(Item, pk=pk)
	if request.method == 'POST':
            h = History.objects.get(pk=pk)
            h.type_text = "deleted"
            h.save()
            item.delete()
            return redirect('item_list')
	return render(request, template_name, {'object':item})

def search_results(request, template_name="inventory/search_results.html"):
    data = {}
    query = request.POST.get('query')
    data['results'] = Item.objects.filter(name_text__icontains=query)
    
    return render(request, template_name, data )


def get_items(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        items = Item.objects.filter(name_text__icontains = q )[:15]
        results = []
        for item in items:
            item_json = {}
            item_json['label'] = item.name_text
            item_json['value'] = reverse('item_detail', kwargs={'pk': item.id} )
            results.append(item_json)
        
        data = json.dumps(results)
    else:
        data = 'fail'
    
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
