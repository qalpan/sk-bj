# sk_bj/urls.py
urlpatterns = [
    # Админ панелінің өзі
    path('admin-panel/', TemplateView.as_view(template_name="tөlemesep_smart.html")),
    # Деректерді сақтау және алу (API)
    path('api/data/', views.api_manager),
    # Пайдаланушының жеке түбіртегі (Пәтер ID бойынша)
    path('pater/<str:apt_id>/', views.api_manager, name='pater_detail'),
]
