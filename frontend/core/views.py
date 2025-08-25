from django.shortcuts import render
from core.forms import QueryForm
from core.models import SSR, ISSR, CSSR, VNTR
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .serializers import CSSRModelSerializer, ISSRModelSerializer, SSRModelSerializer, VNTRModelSerializer
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_GET
from .models import CSSR, ISSR, SSR, VNTR
import csv
import json
import io
import zipfile
from django.conf import settings
import os



MODEL_MAP = {
    'cssr':CSSR,
    'issr':ISSR,
    'ssr':SSR,
    'vntr':VNTR
}

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def query(request):
    form = QueryForm()

    if request.method=='POST':
        form = QueryForm(request.POST)

        if form.is_valid():
            sequence_type = form.cleaned_data['sequence_type']

    return render(request, 'core/query.html', {'form':form})



def autocomplete(request):
    if request.method == "POST":
        sequence = request.POST.get("raw_sequence", "")
        sequence_type = request.POST.get("sequence_type", "")  # JS sends this
        if not sequence_type:
            sequence_type = request.POST.get("id_for_sequence_type", "")  # fallback

        debug_info = {
            "raw_sequence": sequence,
            "sequence_type": sequence_type
        }

        results = []

        if sequence_type:
            model = MODEL_MAP.get(sequence_type)
            debug_info["model"] = str(model)
            if model:
                queryset = model.objects.filter(sequence__icontains=sequence) \
                    .values_list('sequence', flat=True).distinct()[:5]
                results = [{'sequence': seq} for seq in queryset]
        else:
            debug_info["model"] = "sequence_type empty"
            # optional: search all models if sequence_type empty
            for key, model in MODEL_MAP.items():
                queryset = model.objects.filter(sequence__icontains=sequence) \
                    .values_list('sequence', flat=True).distinct()[:5]
                results.extend({"sequence": seq} for seq in queryset)

        debug_info["results_count"] = len(results)
        return JsonResponse({"results": results, "debug": debug_info})

    return JsonResponse({"results": [], "debug": {"error": "Invalid request"}}, status=400)




    
def download(request):    
    sequence_type = request.GET.get('sequence_type')
    model = MODEL_MAP.get(sequence_type)

    q_object = Q()
    clade = request.GET.get('clade')
    subclade = request.GET.get('subclade')
    type = request.GET.get('type')
    sequence = request.GET.get('sequence')

    if clade:
        q_object &= Q(clade__icontains=clade)

    if subclade:
        q_object &= Q(clade__icontains=subclade)

    if sequence:
        q_object &= Q(sequence__icontains=sequence)

    if type and type != 'all':
            q_object &= Q(type=type)

    queryset = model.objects.filter(q_object) if q_object else model.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{sequence_type}_results.csv"'

    writer = csv.writer(response)

    # Write header dynamically
    if queryset.exists():
        columns = [field.name for field in model._meta.fields]
        writer.writerow(columns)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in columns])
    else:
        writer.writerow(['No results'])

    return response
    

def faq(request):
    return render(request, 'core/faq.html')

def resources(request):
    return render(request, 'core/resources.html')

def api_documentation(request):
    return render(request, 'core/api_documentation.html')

def contact(request):
    return render(request, 'core/contact.html')


def download_data(request, option):
    # Map options to mounted paths inside the container
    data_paths = {
        'cssr': '/data_cssr',
        'issr': '/data_issr',
        'ssr': '/data_ssr',
        'vntr': '/data_vntr',
    }

    folder_path = data_paths.get(option)
    if not folder_path or not os.path.exists(folder_path):
        raise Http404("Invalid option or folder not found")

    # Collect files
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files:
        raise Http404("No files found for this option")

    # Create zip in memory
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for filename in files:
            file_path = os.path.join(folder_path, filename)
            zip_file.write(file_path, arcname=filename)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{option}_data.zip"'
    return response

####APIs

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100

class CSSRQueryView(APIView):
    pagination_class = StandardResultsSetPagination 

    def get(self, request):

        #by default, return the entire table
        queryset = CSSR.objects.all()
        
        #if fields are selected in the form, apply them in the query
        query_params = self.request.query_params
        q_object = Q()      

        filter_used = False

        clade = query_params.get('clade')
        subclade = query_params.get('subclade')
        sequence = query_params.get('sequence')

        if clade:
            q_object &= Q(clade__icontains=clade)
            filter_used = True

        if subclade:
            q_object &= Q(clade__icontains=subclade)
            filter_used=True

        if sequence:
            q_object &= Q(sequence__icontains=sequence)
            filter_used=True
        
        if filter_used:
            queryset = queryset.filter(q_object)

        

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = CSSRModelSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CSSRModelSerializer(queryset, many=True)
        return Response(serializer.data)
    
class ISSRQueryView(APIView):
    pagination_class = StandardResultsSetPagination 

    def get(self, request):

        #by default, return the entire table
        queryset = ISSR.objects.all()
        
        #if fields are selected in the form, apply them in the query
        query_params = self.request.query_params
        q_object = Q()      

        filter_used = False

        clade = query_params.get('clade')
        subclade = query_params.get('subclade')
        type = query_params.get('type')
        sequence = query_params.get('sequence')

        if clade:
            q_object &= Q(clade__icontains=clade)
            filter_used = True

        if subclade:
            q_object &= Q(clade__icontains=subclade)
            filter_used=True

        if sequence:
            q_object &= Q(sequence__icontains=sequence)
            filter_used=True

        if type and type != 'all':
            q_object &= Q(type=type)
            filter_used=True

        
        if filter_used:
            queryset = queryset.filter(q_object)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = ISSRModelSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ISSRModelSerializer(queryset, many=True)
        return Response(serializer.data)
    
class SSRQueryView(APIView):
    pagination_class = StandardResultsSetPagination  # just the class, no ()

    def get(self, request):

        #by default, return the entire table
        queryset = SSR.objects.all()
        
        #if fields are selected in the form, apply them in the query
        query_params = self.request.query_params
        q_object = Q()      

        filter_used = False

        clade = query_params.get('clade')
        subclade = query_params.get('subclade')
        type = query_params.get('type')
        sequence = query_params.get('sequence')

        if clade:
            q_object &= Q(clade__icontains=clade)
            filter_used = True

        if subclade:
            q_object &= Q(clade__icontains=subclade)
            filter_used=True

        if sequence:
            q_object &= Q(sequence__icontains=sequence)
            filter_used=True


        
        if type and type != 'all':
            q_object &= Q(type=type)
            filter_used=True

        if filter_used:
            queryset = queryset.filter(q_object)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = SSRModelSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = SSRModelSerializer(queryset, many=True)
        return Response(serializer.data)
    
class VNTRQueryView(APIView):
    pagination_class = StandardResultsSetPagination  # just the class, no ()

    def get(self, request):

        #by default, return the entire table
        queryset = VNTR.objects.all()
        
        #if fields are selected in the form, apply them in the query
        query_params = self.request.query_params
        q_object = Q()      

        filter_used = False

        clade = query_params.get('clade')
        subclade = query_params.get('subclade')
        sequence = query_params.get('sequence')


        if clade:
            q_object &= Q(clade__icontains=clade)
            filter_used = True

        if subclade:
            q_object &= Q(clade__icontains=subclade)
            filter_used=True

        if sequence:
            q_object &= Q(sequence__icontains=sequence)
            filter_used=True
        
        if filter_used:
            queryset = queryset.filter(q_object)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)

        if page is not None:
            serializer = VNTRModelSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = VNTRModelSerializer(queryset, many=True)
        return Response(serializer.data)
    

