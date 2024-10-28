from django.shortcuts import render
import json
from pyexpat import model
from venv import logger
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from grpc import Status
from requests import request
from myapp.models import User,Produit,Client,Categorie,SousCategorie,Cart,CartItem
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny, IsAuthenticated
from myapp.serializers import UserSerializer, CustomTokenObtainPairSerializer,ClientSerializer,ProduitSerializer,CategorieSerializer,SousCategorieSerializer,CartSerializer,CartItemSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm
from django.contrib import messages

class LoginViews(APIView):
    permission_classes = [AllowAny] 
    def index_view(request):
        return render(request, 'index.html')
    def indexAdmin_view(request):
        return render(request, 'indexAdmin.html')
    def categories_view(request):
        return render(request, 'categories.html')
    def SousCategories_view(request):
        return render(request, 'SousCategories.html')
    def produits_view(request):
        return render(request, 'produits.html')
    def shop_view(request):
        return render(request, 'shop.html')
    def signup_view(request):
        return render(request, 'signup.html')
    def signupClient_view(request):
        return render(request, 'signupClient.html') 
    def loginClient_view(request):
        return render(request, 'loginClient.html') 
    def signup(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            cin = request.POST.get('cin')
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            age = request.POST.get('age')
            adresse = request.POST.get('adresse')
            télé = request.POST.get('télé')

            if not email:
                return HttpResponse({'error': 'Email is required'}, status=400)
            if not password:
                return HttpResponse({'error': 'Password is required'}, status=400)
            # Validate other required fields as needed

            try:
                user = User.objects.get(email=email)
                return HttpResponse({'error': 'User with this email already exists.'}, status=400)
            except User.DoesNotExist:
                hashed_password = make_password(password)
                user = User.objects.create(
                    email=email,
                    password=hashed_password,
                    cin=cin,
                    nom=nom,
                    prenom=prenom,
                    age=age,
                    adresse=adresse,
                    télé=télé
                )
                serializer = UserSerializer(user)
                return HttpResponse({'message': 'User created successfully', 'user': serializer.data}, status=201)
                
        else:
             return render(request, 'signup.html')

    def login_view(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None:
                if check_password(password, user.password):
                    request.session['user_id'] = user.user_id
                    return HttpResponseRedirect('/index/')  # Redirect to '/index/' upon successful login
                else:
                    return HttpResponse("Invalid login credentials. Please try again.")
            else:
                return HttpResponse("Invalid login credentials. Please try again.")

        return render(request, 'login.html')

  
    def put(self, request):
        data = request.data.copy()
        email = data.get('email')
        user_id = data.get('user_id')

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)

        # Check if the provided email is different from the current email of the user
        if email != user.email and User.objects.filter(email=email).exists():
            return Response({'error': 'User with this email already exists.'}, status=400)

        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        return Response({'user': user_data}, status=200)

    def delete(self, request, user_id=None):
        user_id = request.query_params.get('user_id')
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        user.delete()
        return Response("User deleted successfully", status=200)
    
# pour client 
class ClientViews(APIView):
    permission_classes = [AllowAny]

    def signupClient(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            cin = request.POST.get('cin')
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            age = request.POST.get('age')
            adresse = request.POST.get('adresse')
            télé = request.POST.get('télé')
            sexe = request.POST.get('sexe')

            if not email:
                return HttpResponse({'error': 'Email is required'}, status=400)
            if not password:
                return HttpResponse({'error': 'Password is required'}, status=400)
            # Validate other required fields as needed

            try:
                client = Client.objects.get(email=email)
                return HttpResponse({'error': 'Client with this email already exists.'}, status=400)
            except Client.DoesNotExist:
                hashed_password = make_password(password)
                client = Client.objects.create(
                    email=email,
                    password=hashed_password,  # Add this field to your model if required
                    cin=cin,
                    nom=nom,
                    prenom=prenom,
                    age=age,
                    adresse=adresse,
                    télé=télé,
                    sexe=sexe,
                )
                serializer = ClientSerializer(client)
                return HttpResponse({'message': 'Client created successfully', 'user': serializer.data}, status=201)
                
        else:
            return render(request, 'signupClient.html')

    def loginClient_view(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                client = Client.objects.get(email=email)
            except Client.DoesNotExist:
                client = None

            if client is not None:
                if check_password(password, client.password):  # Assuming password is stored in the Client model
                    request.session['client_id'] = client.idCli
                    return HttpResponseRedirect('/index/')  # Redirect to '/index/' upon successful login
                else:
                    return HttpResponse("Invalid login credentials. Please try again.")
            else:
                return HttpResponse("Invalid login credentials. Please try again.")

        return render(request, 'loginClient.html')

    def put(self, request):
        data = request.data.copy()
        email = data.get('email')
        client_id = data.get('client_id')

        try:
            client = Client.objects.get(idCli=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found.'}, status=404)

        # Check if the provided email is different from the current email of the user
        if email != client.email and Client.objects.filter(email=email).exists():
            return Response({'error': 'Client with this email already exists.'}, status=400)

        serializer = ClientSerializer(client, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        client_data = serializer.data

        return Response({'client': client_data}, status=200)

    def delete(self, request, client_id=None):
        client_id = request.query_params.get('client_id')
        try:
            client = Client.objects.get(idCli=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=404)
        client.delete()
        return Response("Client deleted successfully", status=200)

# pour catégorie

class CategorieViews(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        categories = Categorie.objects.all()
        serializer = CategorieSerializer(categories, many=True)
        return render(request, 'categories.html', {'categories': serializer.data})
    def add_category(request):
        if request.method == 'POST':
            nom_cate = request.POST.get('nom_cate')
            categorie = Categorie.objects.create(nom_cate=nom_cate)
            serializer = CategorieSerializer(categorie)
            return redirect('/categories/')  
        else:
            return render(request, 'add_category.html')            

  
    def update(self, request):
        data = request.data.copy()
        code_cate = data.get('code_cate')

        try:
            categorie = Categorie.objects.get(code_cate=code_cate)
        except Categorie.DoesNotExist:
            return Response({'error': 'Categorie not found.'}, status=404)

        serializer = CategorieSerializer(categorie, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        categorie_data = serializer.data

        return Response({'categorie': categorie_data}, status=200)
    def update_category(request, code_cate):
        category = get_object_or_404(Categorie, code_cate=code_cate)

        if request.method == 'POST':
            # Retrieve the updated category name from the form data
            new_name = request.POST.get('nom_cate')
            
            # Update the category name
            category.nom_cate = new_name
            category.save()
            
            return redirect('/categories/')
        else:
            return render(request, 'update_category.html', {'categories': category})
    def delete_category(request, code_cate):
        category = get_object_or_404(Categorie, code_cate=code_cate)

        if request.method == 'POST':
            # If the user confirms deletion, delete the category
            if 'confirm_delete' in request.POST:
                category.delete()
                return redirect('/categories/')
            # If the user cancels deletion, redirect back to the category list page
            elif 'cancel_delete' in request.POST:
                return redirect('/categories/')
        else:
            # Render the confirmation template
            return render(request, 'delete_category.html', {'categories': category})
        
#pour sous catégories

class SousCategorieViews(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        souscategories = SousCategorie.objects.all()
        serializer = SousCategorieSerializer(souscategories, many=True)
        return render(request, 'souscategories.html', {'souscategories': serializer.data})
    def add_sous_category(request):
        if request.method == 'POST':
            nom_sous_cate = request.POST.get('nom_sous_cate')
            code_cate = request.POST.get('code_cate')  # Retrieve code_cate from POST data

            try:
                # Retrieve the actual Categorie instance using the id
                categorie = Categorie.objects.get(code_cate=code_cate)
 
                # Create a new SousCategorie instance
                souscategorie = SousCategorie.objects.create(
                    nom_sous_cate=nom_sous_cate,
                    categorie=categorie,

                )

                return redirect('/SousCategories/')  # Redirect to the category list page after adding

            except Categorie.DoesNotExist:
                # Handle the case where the category does not exist
                return render(request, 'add_sous_category.html', {'error': 'Category not found'})

        else:
            categories = Categorie.objects.all()
            return render(request, 'add_sous_category.html', {'categories': categories})

                
            
    def update_sous_category(request, code_Souscate):
        souscategorie = get_object_or_404(SousCategorie, code_Souscate=code_Souscate)

        if request.method == 'POST':
            # Retrieve the updated category name from the form data
            new_name = request.POST.get('nom_sous_cate')  # Removed extra space
            
            # Update the category name
            souscategorie.nom_sous_cate = new_name
            souscategorie.save()
            
            return redirect('/SousCategories/')
        else:
            return render(request, 'update_sous_category.html', {'souscategorie': souscategorie})


    def delete_sous_category(request, code_Souscate):
        souscategories = get_object_or_404(SousCategorie, code_Souscate=code_Souscate)

        if request.method == 'POST':
            # If the user confirms deletion, delete the category
            if 'confirm_delete' in request.POST:
                souscategories.delete()
                return redirect('/SousCategories/')
            # If the user cancels deletion, redirect back to the category list page
            elif 'cancel_delete' in request.POST:
                return redirect('/SousCategories/')
        else:
            # Render the confirmation template
            return render(request, 'delete_sous_category.html', {'SousCategories': souscategories})
#pour produit
class ProduitViews(APIView):
    permission_classes = [AllowAny] 
    def get(request):
        produits = Produit.objects.all() 
        serializer = ProduitSerializer(produits, many=True)
        return render(request, 'produits.html', {'produits': serializer.data})
    def add_produit(request):
        if request.method == 'POST':
            nom = request.POST.get('nom')
            description = request.POST.get('description')
            prix = request.POST.get('prix')
            qteTotal = request.POST.get('qteTotal')
            user_id = request.POST.get('user_id')
            code_cate = request.POST.get('code_cate')
            code_Souscate = request.POST.get('code_Souscate')
            image = request.FILES.get('image')

            # Get User and Categorie instances
            user = User.objects.get(pk=user_id)
            categorie = Categorie.objects.get(code_cate=code_cate)
            sousCategorie = SousCategorie.objects.get(code_Souscate=code_Souscate)

            # Create Produit instance and save to the database
            produit = Produit.objects.create(
                nom=nom,
                description=description,
                prix=prix,
                qteTotal=qteTotal,
                user=user,
                categorie=categorie,
                sousCategorie=sousCategorie,
                image=image,
            )

            return redirect('/produits/')  # Redirect after successful form submission
        else:
            users = User.objects.all()
            categories = Categorie.objects.all()
            sousCategories = SousCategorie.objects.all()
            return render(request, 'add_produit.html', {'users': users, 'categories': categories, 'sousCategories':sousCategories})

    def update_produit(request, idProd):
        produit = get_object_or_404(Produit, pk=idProd)

        if request.method == 'POST':
            nom = request.POST.get('nom')
            description = request.POST.get('description')
            prix = request.POST.get('prix')
            qteTotal = request.POST.get('qteTotal')
            user_id = request.POST.get('user_id')
            code_cate = request.POST.get('code_cate')
            code_Souscate = request.POST.get('code_Souscate')
            image = request.FILES.get('image')

            print("Form data received:")
            print("Nom:", nom)
            print("Description:", description)
            print("Prix:", prix)
            print("QteTotal:", qteTotal)
            print("User ID:", user_id)
            print("Category Code:", code_cate)
            print("Sous Category:", code_Souscate)
            print("Image:", image)

            try:
                # Get User and Categorie instances
                user = User.objects.get(pk=user_id)
                categorie = Categorie.objects.get(code_cate=code_cate)
                sousCategorie = SousCategorie.objects.get(code_Souscate=code_Souscate)

                # Update fields
                produit.nom = nom
                produit.description = description
                produit.prix = prix
                produit.qteTotal = qteTotal
                produit.user = user
                produit.categorie = categorie
                produit.sousCategorie = sousCategorie

                # Update image if provided
                if image:
                    print("Updating image...")
                    produit.image = image

                produit.save()
                print("Product updated successfully.")

                return redirect('/produits/')  # Redirect after successful form submission
            except User.DoesNotExist:
                return HttpResponseBadRequest("User does not exist.")
            except Categorie.DoesNotExist:
                return HttpResponseBadRequest("Category does not exist.")
            except SousCategorie.DoesNotExist:
                return HttpResponseBadRequest("Sous-category does not exist.")
        else:
            users = User.objects.all()
            categories = Categorie.objects.all()
            sousCategories = SousCategorie.objects.all()
            return render(request, 'update_produit.html', {'produit': produit, 'users': users, 'categories': categories, 'sousCategories': sousCategories})
    def delete_produit(request, idProd):
        produit = get_object_or_404(Produit, idProd=idProd)

        if request.method == 'POST':
            # If the user confirms deletion, delete the category
            if 'confirm_delete' in request.POST:
                produit.delete()
                return redirect('/produits/')
            # If the user cancels deletion, redirect back to the category list page
            elif 'cancel_delete' in request.POST:
                return redirect('/produits/')
        else:
            # Render the confirmation template
            return render(request, 'delete_produit.html', {'produit': produit})
    def search_products(request):
        query = request.GET.get('query', '')  # Provide a default empty string if `query` is None
        produits = Produit.objects.filter(nom__icontains=query)  # Use icontains for case-insensitive search
        
        # Pagination
        paginator = Paginator(produits, 3)  # Show 3 products per page
        page = request.GET.get('page', 1)
        try:
            produits_page = paginator.page(page)
        except PageNotAnInteger:
            produits_page = paginator.page(1)
        except EmptyPage:
            produits_page = paginator.page(paginator.num_pages)
        
        context = {
            'produits': produits_page,
        }

        return render(request, 'more_products.html', context)
    def get(self, request):
        produits = Produit.objects.all()
        
        # Pagination
        paginator = Paginator(produits, 10)  # Show 2 produits per page
        page = request.GET.get('page', 1)
        try:
            produits_page = paginator.page(page)
        except PageNotAnInteger:
            produits_page = paginator.page(1)
        except EmptyPage:
            produits_page = paginator.page(paginator.num_pages)
        
        serializer = ProduitSerializer(produits_page, many=True)
        
        return render(request, 'produits.html', {'produits': produits_page, 'serializer_data': serializer.data})

    def list_produits(request):
        produits = Produit.objects.all()
        
        # Pagination
        paginator = Paginator(produits, 3)  # Show 2 produits per page
        page = request.GET.get('page', 1)
        try:
            produits_page = paginator.page(page)
        except PageNotAnInteger:
            produits_page = paginator.page(1)
        except EmptyPage:
            produits_page = paginator.page(paginator.num_pages)
        
        serializer = ProduitSerializer(produits_page, many=True)
        
        return render(request, 'store.html', {'produits': produits_page, 'serializer_data': serializer.data})
    def product_detail(request,idProd):
        # Retrieve the product by its primary key (idProd)
        produit = get_object_or_404(Produit, pk=idProd)

        # Add the Euro price to the product object or pass it separately
        context = {
            'produit': produit,
            
        }
        return render(request, 'product_detail.html', context)
    def more_products(request):
        query = request.GET.get('query', '')
        sort_by = request.GET.get('sort', 'idProd')  # Default sorting by product ID

        produits = Produit.objects.filter(nom__icontains=query).order_by(sort_by)
        
        # Pagination
        paginator = Paginator(produits, 3)  # Show 3 products per page
        page = request.GET.get('page', 1)
        try:
            produits_page = paginator.page(page)
        except PageNotAnInteger:
            produits_page = paginator.page(1)
        except EmptyPage:
            produits_page = paginator.page(paginator.num_pages)
        
        context = {
            'produits': produits_page,
            'current_sort': sort_by,  # Pass the current sort option to the template
        }

        return render(request, 'more_products.html', context)
    """def add_to_cart(request, idProd):
        product = get_object_or_404(Produit, idProd=idProd)
        
        # Get the cart from the session or create an empty one if it doesn't exist
        cart = request.session.get('cart', {})

        if str(idProd) in cart:
            cart[str(idProd)]['quantity'] += 1  # Increase the quantity if the item is already in the cart
        else:
            cart[str(idProd)] = {
                'product_name': product.nom,
                'quantity': 1,
                'price': product.prix,
                'image': product.image.url  # Assuming you have an image field in Produit
            }
        
        # Save the updated cart back to the session
        request.session['cart'] = cart

        return redirect('cart')"""
    def add_to_cart(request, idProd):
            product = get_object_or_404(Produit, idProd=idProd)
            cart, created = Cart.objects.get_or_create(client=request.client)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return redirect('cart')
    def update_cart(request, idProd):
            if request.method == 'POST':
                cart = request.session.get('cart', {})
                quantity = int(request.POST.get('quantity', 1))

                if str(idProd) in cart:
                    if quantity > 0:
                        cart[str(idProd)]['quantity'] = quantity  # Update quantity
                    else:
                        del cart[str(idProd)]  # Remove the item if quantity is set to 0 or negative

                request.session['cart'] = cart

            return redirect('cart')
    def cart(request):
            cart = request.session.get('cart', {})
            
            for item_id, item in cart.items():
                item['total_price'] = item['quantity'] * item['price']
            
            total_price = sum(item['total_price'] for item in cart.values())
            
            return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})
    def checkout(request):
        if request.method == 'POST':
            form = CheckoutForm(request.POST)
            if form.is_valid():
                client_data = form.cleaned_data

                # Create or get the client
                client, created = Client.objects.get_or_create(
                    email=client_data['email'],
                    defaults=client_data
                )
                if not created:
                    # Update client details if they already exist
                    for attr, value in client_data.items():
                        setattr(client, attr, value)
                    client.save()

                # Create a cart for the client
                cart = Cart.objects.create(client=client)

                # Get cart items from the session
                cart_items = request.session.get('cart', {})

                if not cart_items:
                    messages.error(request, "Your cart is empty.")
                    return redirect('cart')

                # Loop through cart items and create CartItem objects
                for item_id, quantity in cart_items.items():
                    product = get_object_or_404(Produit, idProd=item_id)

                    # Ensure quantity is an integer and positive
                    if isinstance(quantity, int) and quantity > 0:
                        CartItem.objects.create(
                            cart=cart,
                            product=product,
                            quantity=quantity,
                            price=product.prix  # Assumes price is fetched from the product model
                        )
                    else:
                        # Handle cases where quantity is not valid
                        messages.error(request, f"Invalid quantity detected for product: {product.nom}.")
                        return redirect('cart')

                # Clear the cart from the session
                request.session['cart'] = {}

                # Redirect to confirmation page
                messages.success(request, "Your order has been placed successfully.")
                return redirect('checkout_confirmation')

        else:
            form = CheckoutForm()

        return render(request, 'checkout.html', {'form': form})

    def checkout_confirmation(request):
            return render(request, 'checkout_confirmation.html')


    def more_products(request):
        # Retrieve all products from the database
        produits = Produit.objects.all().order_by('-idProd')
        
        # Pagination
        paginator = Paginator(produits, 10)  # Show 10 products per page
        page = request.GET.get('page', 1)
        try:
            produits_page = paginator.page(page)
        except PageNotAnInteger:
            produits_page = paginator.page(1)
        except EmptyPage:
            produits_page = paginator.page(paginator.num_pages)
        
        context = {
            'produits': produits_page,
        }

        return render(request, 'more_products.html', context)

    def remove_from_cart(request, idProd):
            # Retrieve the cart from the session
            cart = request.session.get('cart', {})

            # Debug print statements
            print("Cart before removal:", cart)
            print("Trying to remove item with idProd:", idProd)

            # Remove the item if it exists in the cart
            if str(idProd) in cart:  # Ensure idProd is converted to string if keys are stored as strings
                del cart[str(idProd)]  # Ensure idProd is converted to string if keys are stored as strings
                print("Item removed. Cart after removal:", cart)
            else:
                print("Item not found in cart.")

            # Save the updated cart back to the session
            request.session['cart'] = cart
            return redirect('cart')