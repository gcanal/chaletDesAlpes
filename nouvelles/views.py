#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from datetime import datetime
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from nouvelles.models import Nouvelle
from nouvelles.forms import ModifyNouvelleTextForm, ModifyNouvelleImageForm, NouvelleForm

#####################    View for the application nouvelles  #####################

def homeNouvelles(request):
    """ Afficher toutes les dernieres nouvelles du site """
    nouvelles = Nouvelle.objects.all() # Nous sélectionnons toutes nos nouvelles
    return render(request, 'nouvelles/accueilNouvelles.html', {'dernieres_nouvelles':nouvelles})
   
def read(request, idNouvelle):
	read=True
	dernieresNouvelles=Nouvelle.objects.order_by('-date')
	nouvelle = get_object_or_404(Nouvelle, id=idNouvelle)
	return render(request, 'nouvelles/NouvelleDisplay.html', locals())

	date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de parution")
	link=models.CharField(max_length=100)
	linkText=models.CharField(max_length=100)

@permission_required("perms.nouvelles.change_nouvelle")
def modifyNouvelleText(request,idNouvelle,lan):
	modifyText=True;read=False;
	nouvelle = get_object_or_404(Nouvelle, id=idNouvelle);
	form=ModifyNouvelleTextForm();
	if request.method=='POST':
		form=ModifyNouvelleTextForm(request.POST)
		if form.is_valid():
			titre=form.cleaned_data['titre'];resume=form.cleaned_data['resume'];paragraphe=form.cleaned_data['paragraphe'];
			legende=form.cleaned_data['legende'];link=form.cleaned_data['link'];linkText=form.cleaned_data['linkText'];
			if lan=='fr':
				nouvelle.titre_fr=titre;nouvelle.paragraphe_fr=paragraphe;nouvelle.legende_fr=legende;nouvelle.link=link;nouvelle.linkText_fr=linkText;
				nouvelle.resume_fr=resume;nouvelle.modifiedInFr=True;
				nouvelle.save(update_fields=['titre_fr','paragraphe_fr','legende_fr','link','linkText_fr','resume_fr','modifiedInFr'])
			else:#in english please
				nouvelle.titre_en=titre;nouvelle.paragraphe_en=paragraphe;nouvelle.legende_en=legende;nouvelle.link=link;nouvelle.linkText_en=linkText;
				nouvelle.resume_en=resume;nouvelle.modifiedInFr=False;nouvelle.translated=True;
				nouvelle.save(update_fields=['titre_en','paragraphe_en','legende_en','link','linkText_en','resume_en','modifiedInFr','translated'])
			dernieresNouvelles=Nouvelle.objects.order_by('-date')
			return redirect('nouvelles.views.read',idNouvelle=nouvelle.id)
	else:
		if lan=='fr':
			form=ModifyNouvelleTextForm(initial={'titre': nouvelle.titre_fr,'paragraphe' : nouvelle.paragraphe_fr,'legende' : nouvelle.legende_fr,
			'link':nouvelle.link,'linkText':nouvelle.linkText_fr,'resume':nouvelle.resume_fr})
		else:#lan='en'
			form=ModifyNouvelleTextForm(initial={'titre': nouvelle.titre_en,'paragraphe' : nouvelle.paragraphe_en,'legende' : nouvelle.legende_en,
			'link':nouvelle.link,'linkText':nouvelle.linkText_en,'resume':nouvelle.resume_en})
	return render(request, 'nouvelles/NouvelleDisplay.html', locals())

@permission_required("perms.nouvelles.change_nouvelle")	
def modifyNouvelleImage(request,idNouvelle):
	modifiyImage=True
	read=False
	nouvelle = get_object_or_404(Nouvelle, id=idNouvelle)
	if request.method=='POST':
		form=ModifyNouvelleImageForm(request.POST,request.FILES,)
		if form.is_valid():
			image=form.cleaned_data['image']
			nouvelle.image=image;
			nouvelle.save(update_fields=['image'])
			dernieresNouvelles=Nouvelle.objects.order_by('-date')
			return redirect('nouvelles.views.read',idNouvelle=nouvelle.id)
	else:
		form=ModifyNouvelleImageForm()
	return render(request, 'nouvelles/NouvelleDisplay.html', locals())

@permission_required("perms.nouvelles.delete_nouvelle")		
def deleteNouvelle(request,idNouvelle):
	delete=True
	nouvelle = get_object_or_404(Nouvelle, id=idNouvelle)
	nouvelle.delete()
	dernieresNouvelles=Nouvelle.objects.order_by('-date')
	return render(request, 'nouvelles/NouvelleDisplay.html', locals())
   
@permission_required("perms.nouvelles.add_nouvelle")	
def createNouvelle(request):
	create=True;read=False
	dernieresNouvelles=Nouvelle.objects.order_by('-date')
	if request.method=='POST':
		form=NouvelleForm(request.POST,request.FILES,)
		if form.is_valid():
			nouvellePageId=form.cleaned_data['nouvellePageId']
			titre=form.cleaned_data['titre']
			resume=form.cleaned_data['resume']
			paragraphe=form.cleaned_data['paragraphe']
			legende=form.cleaned_data['legende']
			link=form.cleaned_data['link']
			linkText=form.cleaned_data['linkText']
			image=form.cleaned_data['image']
			nouvelle=Nouvelle(nouvellePageId=nouvellePageId,titre_fr=titre,paragraphe_fr=paragraphe,image=image,legende_fr=legende,link=link,linkText_fr=linkText,resume_fr=resume,translated=False,modifiedInFr=True)
			nouvelle.save()
			return redirect('nouvelles.views.read',idNouvelle=nouvelle.id)
	else:
		form=NouvelleForm()
	return render(request, 'nouvelles/NouvelleDisplay.html', locals())
