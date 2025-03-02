import io
from django.shortcuts import render
from hospital import forms, models
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import random


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



def generate_charts(request):
    # Sample user ages
    sample_ages = [15, 22, 35, 55, 29, 42, 18, 33, 26, 50, 17, 45, 60, 39, 23, 41, 20, 30]

    # Categorize ages
    age_groups = {"0-18": 0, "19-30": 0, "31-50": 0, "51+": 0}
    for age in sample_ages:
        if age <= 18:
            age_groups["0-18"] += 1
        elif age <= 30:
            age_groups["19-30"] += 1
        elif age <= 50:
            age_groups["31-50"] += 1
        else:
            age_groups["51+"] += 1

    # 📊 Bar Chart (User Age Groups)
    bar_fig = go.Figure([go.Bar(x=list(age_groups.keys()), y=list(age_groups.values()), marker_color='blue')])
    bar_chart = bar_fig.to_html(full_html=False, include_plotlyjs='cdn')

    # 🥧 Pie Chart (User Age Distribution)
    pie_fig = go.Figure([go.Pie(labels=list(age_groups.keys()), values=list(age_groups.values()))])
    pie_chart = pie_fig.to_html(full_html=False, include_plotlyjs='cdn')

    # 🌍 Map Graph (Random User Locations)
    locations = pd.DataFrame({
        "latitude": [random.uniform(-90, 90) for _ in range(10)],
        "longitude": [random.uniform(-180, 180) for _ in range(10)]
    })
    map_fig = px.scatter_geo(locations, lat="latitude", lon="longitude", title="User Locations (Random)")
    map_chart = map_fig.to_html(full_html=False, include_plotlyjs='cdn')

    return render(request, 'hospital/other/try.html', {
        'pie_chart': pie_chart,
        'bar_chart': bar_chart,
        'map_chart': map_chart
    })
    
def age_pie_chart(request):
    # Sample user ages (hardcoded)
    sample_ages = [15, 22, 35, 55, 29, 42, 18, 33, 26, 50, 17, 45, 60, 39, 23, 41, 20, 30]

    # Categorize ages
    age_groups = {
        "0-18": 0,
        "19-30": 0,
        "31-50": 0,
        "51+": 0
    }

    for age in sample_ages:
        if age <= 18:
            age_groups["0-18"] += 1
        elif age <= 30:
            age_groups["19-30"] += 1
        elif age <= 50:
            age_groups["31-50"] += 1
        else:
            age_groups["51+"] += 1

    # Create a Plotly pie chart
    fig = px.pie(
        names=age_groups.keys(),
        values=age_groups.values(),
        title="User Age Distribution",
    )
    
    # Convert the chart to HTML
    graph = fig.to_html(full_html=False)

    return render(request, 'hospital/other/try.html', {'graph': graph})    