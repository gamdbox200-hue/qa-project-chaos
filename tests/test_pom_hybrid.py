def test_hybrid_with_pom(api_request_context, users_page):
    # 1. API часть (логика данных)
    user = api_request_context.get("/users/3").json()
    target_name = user["name"] # Clementine Bauch

    # 2. UI часть (логика страницы)
    users_page.navigate()
    users_page.verify_user_exists(target_name)