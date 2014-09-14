#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from datetime import datetime
from django.contrib.auth.models import User	
from django.contrib.auth.decorators import permission_required
from blog.models import Article, Category
from blog.forms import ArticleForm, CategoryForm, ArticleImageForm, ArticleTextForm

#####################    View for the application blog  #####################

#TODO improve redirection after forms

#displays the blog home page when no articles are selected
def home(request):
	lastArticles=Article.objects.all();
	categories=Category.objects.all();
	n=categories.count();
	if n == 0:
		if request.user.has_perm('blog.website.add_category'):
			return addCategory(request)
		else:
			return redirect('website.views.home');
	else:
		firstCategory= categories[0]
		return page(request, firstCategory.id)

def page(request, idCategoryAsked):
	lastArticles=Article.objects.all();
	categories=Category.objects.all();
	category=Category.objects.get(id=idCategoryAsked);
	articles=Article.objects.filter(category__id=idCategoryAsked);
	idCategory=str(idCategoryAsked);
	#check if asked category exists
	#import re, string; pattern = re.compile('[\W_]+')" \
    #pattern.sub('', string.printable)" 
	return render(request, 'blog/homeBlog.html', locals());
	
	#articles=Article.objects.filter(category=categoryAsked).order_by('date');
	#return render(request, pageIdToTemplate(pageIdAsked),locals(),context_instance=RequestContext(request))
	

def addArticle(request):
	categories=Category.objects.all();
	if request.method=='POST':
		form=ArticleForm(request.POST,request.FILES)
		if form.is_valid():
			title=form.cleaned_data['title'];summary=form.cleaned_data['summary'];paragraph=form.cleaned_data['paragraph']
			caption=form.cleaned_data['caption'];link=form.cleaned_data['link'];linkText=form.cleaned_data['linkText'];
			image=form.cleaned_data['image'];category=form.cleaned_data['category'];
			envoi=True
			#creation of the section object
			article=Article(title=title,summary=summary,paragraph=paragraph,caption=caption,image=image,link=link,linkText=linkText)
			article.category=category;
			article.save();
			return home(request);
			#return page(request,category);
	else:
		addArticle=True;
		displayForm=True;
		form=ArticleForm()
	return render(request, 'blog/blogForm.html',locals())
		
def addCategory(request):
	categories=Category.objects.all();
	addCategory=True;
	displayForm=True;	
	if request.method=='POST':
		form=CategoryForm(request.POST)
		if form.is_valid():
			title=form.cleaned_data['title'];
			envoi=True
			#creation of the section object
			category=Category(title=title)
			category.save();
			return home(request)
	else:
		form=CategoryForm()
	return render(request, 'blog/blogForm.html',locals())		
			
def renameCategory(request,idCategory):
	categories=Category.objects.all();
	cat=Category.objects.get(id=idCategory)
	displayForm=True;	
	if request.method=='POST':
		form=CategoryForm(request.POST)
		if form.is_valid():
			title=form.cleaned_data['title'];
			cat.title=title
			cat.save();
			return page(request,idCategory)
	else:
		form=CategoryForm(initial={'title': cat.title,})
	return render(request, 'blog/blogForm.html',locals())

@permission_required("perms.blog.change_article")		
def modifyArticleText(request,idAsked):#modifies the section of the given pageId in the given position
	categories=Category.objects.all();
	textModification=True;
	art=Article.objects.get(id=idAsked)#get return an object , filter a queryset
	if request.method=='POST':
		form=ArticleTextForm(request.POST)
		if form.is_valid():
			art.title=form.cleaned_data['title'];art.paragraph=form.cleaned_data['paragraph'];art.caption=form.cleaned_data['caption'];
			art.link=form.cleaned_data['link'];art.linkText=form.cleaned_data['linkText'];
			art.save();		
			return home(request);
	else:#Get method
		displayForm=True;
		form=ArticleTextForm(title=art.title,paragraph=art.paragraph,caption=art.caption,link=art.link,linkText=art.linkText)	 
		return render(request,'blog/blogForm.html',locals())

@permission_required("perms.blog.change_article")		 
def modifyArticleImage(request,idAsked):
	categories=Category.objects.all();
	imageModification=True # flag for the template
	art=Article.objects.get(id=idAsked)#get return an object , filter a queryset
	if request.method=='POST':
		form=ArticleImageForm(request.POST,request.FILES)
		if form.is_valid():
			image=form.cleaned_data['image']
			art.image=image;art.save(update_fields=['image'])
			return home(request)
	else:
		displayForm=True;
		form=ArticleImageForm()	 
		return render(request,'blog/blogForm.html',locals())
			
@permission_required("perms.blog.delete_article")		
def deleteArticle(request,idAsked): #deletes the section of the given pageId in the given position
	categories=Category.objects.all();
	art=Article.objects.filter(id=idAsked)
	art.delete()
	return home(request)
	
def deleteCategoryWithConfirmation(request, idAsked):
	categories=Category.objects.all();
	idCategory=idAsked;
	confirmDeleteCategory=True
	cat=Category.objects.get(id=idAsked)
	n_articles=Article.objects.filter(category__id=idAsked).count();
	return render(request,'blog/blogForm.html',locals())
	
   ############## here TODO understand why category.title does not appear in the template ##############
def deleteCategory(request, idAsked):
	categories=Category.objects.all();
	idAsked=int(idAsked);
	category=Category.objects.get(id=idAsked);
	articles=Article.objects.filter(category__id=idAsked);
	articles.delete();
	category.delete();
	return home(request)
	
"""

@permission_required("perms.nouvelles.change_nouvelle")	
def modifyArticleImage(request,idArticle):
	modifiyImage=True
	read=False
	article = get_object_or_404(Nouvelle, id=idArticle)
	if request.method=='POST':
		form=ModifyNouvelleImageForm(request.POST,request.FILES,)
		if form.is_valid():
			image=form.cleaned_data['image']
			article.image=image;
			article.save(update_fields=['image'])
			lastArticles=Nouvelle.objects.order_by('-date')
			#return redirect('nouvelles.views.read',idNouvelle=nouvelle.id)
	else:
		form=ModifyNouvelleImageForm()
	return render(request, 'nouvelles/NouvelleDisplay.html', locals())

def render_from_pageId(request,pageIdAsked):
	pageId=int(pageIdAsked)
	nouvelleCounter, created = NouvelleCounter.objects.get_or_create(pageId=pageId,defaults={'counter': 3})
	sections=Section.objects.filter(pageId=pageIdAsked).order_by('position');
	nouvellesSection=Nouvelle.objects.filter(nouvellePageId=pageIdAsked)
	dernieresNouvelles=Nouvelle.objects.order_by('-date')[:nouvelleCounter.counter]# latest Nouvelle Objects limitated to "counter"
	#nNouvelles=min(dernieresNouvelles.count(),counter);#number of news that will be displayed on the page	
	return render(request, pageIdToTemplate(pageIdAsked),locals(),context_instance=RequestContext(request))

def home(request):
    #Afficher toutes les dernieres nouvelles du site#
    nouvelles = Nouvelle.objects.all() # Nous sélectionnons toutes nos nouvelles
    return render(request, 'nouvelles/homeNouvelles.html', {'dernieres_nouvelles':nouvelles})


def appartementDjanEGlyamo(request):
	return render_from_pageId(request,1)
def appartementMestye(request):
	return render_from_pageId(request,2)
def appartementMartna(request):
	return render_from_pageId(request,3)
def plusDuChalet(request):
	return render_from_pageId(request,4)
def coteCosy(request):
	return render_from_pageId(request,5)
def aProximite(request):
	return render_from_pageId(request,6)
def pourVenir(request):
	return render_from_pageId(request,7)

  
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
	
	
	
def pageIdToString(pageId):
	if isinstance( pageId, int ):
		pageId=str(pageId)
	if pageId=='100':
		return "Toutes les nouvelles"
	if pageId=='101':
		return "Appartement DjanEGlyamo"
	if pageId=='102':
		return "Appartement Mestye"
	if pageId=='103':
		return "Appartement Martna"
	if pageId=='104':
		return "Plus du chalet"
	if pageId=='105':
		return "Cote cosy"
	if pageId=='106':
		return "A proximite"
	if pageId=='107':
		return "Pour venir"
	return "undefined pageId"


		
viewsFromId={100: 'nouvelles.views.home',101: 'nouvelles.views.appartementDjanEGlyamo',102:'nouvelles.views.appartementMestye',
103:'nouvelles.views.appartementMartna',104:'nouvelles.views.plusDuChalet',105:'nouvelles.views.coteCosy',106:'nouvelles.views.aProximite',
107:'nouvelles.views.pourVenir',108:'nouvelles.views.reservations',109:'nouvelles.views.contact'}	

"""
