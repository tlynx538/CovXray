"""
All the website views reside here.

Author: Akhil Kokani
"""
from django.shortcuts import render
from django.views import View



class HomeView(View):
    """
    This is the home page view.
    """

    def get(self, request):
        """
        If the request of GET type then render the home page.
        """
        return render(request, "home.html", {})


    def post(self, request):
        """
        If the request is of POST type then following is assumed:
        user is trying to upload an image which is an X-ray scan
        and should be used as an input for detecting COVID-19.
        """
        from django.http import JsonResponse
        from .forms import XrayImageForm
        from .models import XrayImages

        response = {
            "error": None # set this true if any error occurs while processing else false
            , "error_msg": ""
            , "has_covid": None # set this true if COVID detected
            , "is_normal": None # set this true if no COVID and viral detected
            , "has_viral": None # set this true if viral detected
        }

        form = XrayImageForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_image = form.cleaned_data['xray_scan_img']
            
            # create new instance, doing so will ease in accessing uploaded image url
            xray_image = XrayImages()
            xray_image.xray_scan_img = uploaded_image
            xray_image.save()

            # uploaded image url
            uploaded_image_url = xray_image.xray_scan_img.url

            response['error'] = False

            """
            Hey Vinayak,
            
            Invoke ML inference code here using the 'uploaded_image_url' variable.
            Once the inference results are available set the 'response' headers accordingly.
            
            Ex:
                if user has covid:
                    response['has_covid'] = True else False
                elif user has viral:
                    response['has_viral'] = True else False
                elif user is normal:
                    response['is_normal'] = True else False
            
            Just make sure at any instance any one of them should be set to true, say if
            user has covid then set 'has_covid' to true and other two as false.
            
            Once work is done, feel free to delete this comment.
            """

            return JsonResponse(response)
        else:
            response['error'] = True
            response['error_msg'] = "There was an error in your uploaded image. Try again with different image."
            return JsonResponse(response)
