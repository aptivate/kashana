from django_assets import Bundle, register

# Main CSS

alfie_scss = Bundle('scss/alfie.scss',
                  filters='pyscss',
                  output='alfie/alfie.css',
                  depends='scss/**/*.scss')

pure_css = Bundle('css/pure.min.css')
pen_css = Bundle('css/pen.css')
ui_jq_css = Bundle('css/redmond/jquery-ui-1.11.4.custom.min.css')

css_all = Bundle(pure_css, pen_css, ui_jq_css, alfie_scss,
    filters=['cssmin', 'cssrewrite'],
    output='alfie/all.css')

admin_css = Bundle('scss/admin.scss',
                   filters=['pyscss', 'cssmin'],
                   output='alfie/admin.css',
                   depends='scss/**/*.scss')

register('css_all', css_all)
register('css_admin', admin_css)
