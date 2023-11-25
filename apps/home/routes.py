# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from utils.dash import get_data, plot_temporadas, fig_to_base64

@blueprint.route('/index')
@login_required
def index():
    df_check = get_data().get('df_check')
    fig_temporadas=plot_temporadas(df_check, x='temporada', y='rodada', cutoff=38)
    image_data_temporadas = fig_to_base64(fig_temporadas)
    
    temporada_atual='2023'
    rodada_atual='28'
    percentual='75'
    ultima_atualizacao='24/11/2023'

    return render_template('home/index.html', segment='index', 
                                            image_data_temporadas=image_data_temporadas,
                                            temporada_atual=temporada_atual,
                                            rodada_atual=rodada_atual,
                                            percentual=percentual,
                                            ultima_atualizacao=ultima_atualizacao)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
