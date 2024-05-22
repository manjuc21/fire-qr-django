from django.shortcuts import render, redirect
import io
import json
import qrcode
from django.http import JsonResponse,HttpResponse
from .models import VehicleDetails
import base64
from django.shortcuts import get_object_or_404
from datetime import date
from PIL import Image
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)

from django.shortcuts import render

def home1(request):
    return render(request, 'viewqr.html')

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

def get_vehicle_qr_image(request):
    try:
        # Retrieve the registration_number_id from the request
        registration_number_id = request.GET.get('registration_number_id')
        images_dir = os.path.abspath(os.path.join(os.getcwd(), "images"))
        img_path = os.path.join(images_dir, (registration_number_id+".jpg"))
        # Retrieve the VehicleQR object based on the registration_number_id
        
       
        # Serialize the dictionary to JSON

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(img_path)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        with io.BytesIO() as output:
            qr_img.save(output)
            image_data = output.getvalue()

        # Convert the image data to a base64 string
        qr_image_base64 = base64.b64encode(image_data).decode()

        data = {"qr_image": qr_image_base64}
        return render(request, 'home.html', data)

    except Exception as e:
        return HttpResponse(e)


def render_get_qr(request):
    return render(request,'fetch.html')


def store_vehicle_details(request):
    if request.method == 'POST':
        try:
            # Extract all the form data
            registration_number = request.POST.get('registration_number')
            manufactured_by = request.POST.get('manufactured_by')
            vehicle_model = request.POST.get('vehicle_model')
            year_of_manufacture = request.POST.get('year_of_manufacture')
            body_built_by = request.POST.get('body_built_by')
            type_of_vehicle = request.POST.get('type_of_vehicle')
            battery_size = request.POST.get('battery_size')
            tyre_size = request.POST.get('tyre_size')
            chassis_number = request.POST.get('chassis_number')
            engine_number = request.POST.get('engine_number')
            date_of_delivery = request.POST.get('date_of_delivery')
            order_number = request.POST.get('order_number')
            kgid_policy_number = request.POST.get('kgid_policy_number')
            location = request.POST.get('location')

            # Create a VehicleDetails object
            vehicle = VehicleDetails.objects.create(
                registration_number=registration_number,
                manufactured_by=manufactured_by,
                vehicle_model=vehicle_model,
                year_of_manufacture=year_of_manufacture,
                body_built_by=body_built_by,
                type_of_vehicle=type_of_vehicle,
                battery_size=battery_size,
                tyre_size=tyre_size,
                chassis_number=chassis_number,
                engine_number=engine_number,
                date_of_delivery=date_of_delivery,
                order_number=order_number,
                kgid_policy_number=kgid_policy_number,
                location=location
            )

            # Create a dictionary with all the data
            image_path = "fire.jpg"
            with Image.open(image_path) as img:
                    # Resize image if needed
                    img_width, img_height = img.size
                    max_width = 200
                    if img_width > max_width:
                        ratio = max_width / img_width
                        new_height = int(img_height * ratio)
                        img = img.resize((max_width, new_height))

            # Vehicle data
            vehicle_data = {
                        'Registration Number': registration_number,
                        'Manufactured By': manufactured_by,
                        'Vehicle Model': vehicle_model,
                        'Year of Manufacture': year_of_manufacture,
                        'Body Built By': body_built_by,
                        'Type of Vehicle': type_of_vehicle,
                        'Battery Size': battery_size,
                        'Tyre Size': tyre_size,
                        'Chassis Number': chassis_number,
                        'Engine Number': engine_number,
                        'Date of Delivery': date_of_delivery,
                        'Order Number': order_number,
                        'KGID Policy Number': kgid_policy_number,
                        'Location': location
                    }

            # Image size and font settings
            image_width = max(800, img.width + 20)  # Adjust based on image and table width
            row_height = 30
            font = ImageFont.load_default()

            # Calculate image height based on number of rows
            image_height = (len(vehicle_data) + 1) * row_height + img.height + 20  # Add space for the image

            # Create a blank image
            final_img = Image.new('RGB', (image_width, image_height), color='white')
            draw = ImageDraw.Draw(final_img)

            # Paste image onto the final image
            final_img.paste(img, (10, 10))

            # Draw table headers
            x, y = 10, img.height + 30
            for key in vehicle_data.keys():
                draw.rectangle([x, y, x + 200, y + row_height], outline="black")
                draw.text((x + 5, y + 5), key, fill='black', font=font)
                y += row_height

            # Draw table values
            x, y = 210, img.height + 30
            for value in vehicle_data.values():
                draw.rectangle([x, y, x + 200, y + row_height], outline="black")
                draw.text((x + 5, y + 5), value, fill='black', font=font)
                y += row_height

            # Save the image
            images_dir = os.path.abspath(os.path.join(os.getcwd(), "images"))
            print(images_dir)

        # Ensure the directory exists
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)

        # Save the image in the images directory
            img_path = os.path.join(images_dir, (registration_number+".jpg"))
            print(img_path)
  
            final_img.save(img_path)

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(img_path)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            with io.BytesIO() as output:
                qr_img.save(output)
                image_data = output.getvalue()

            # Convert the image data to a base64 string
            qr_image_base64 = base64.b64encode(image_data).decode()

            data = {
                "qr_image": qr_image_base64,
                "message": "Vehicle details of Vehicle stored successfully!",
                "registration number" : registration_number
            }

            # return HttpResponse("Image saved successfully at: " + img_path)

            return render(request, 'home.html', data)  # Redirect after successful creation
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'GET Method not allowed'}, status=405)



def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    else:
        return redirect('home.html')
    



    # Create a blank image
