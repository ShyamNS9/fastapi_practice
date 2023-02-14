from fastapi import FastAPI, APIRouter
from typing import Optional

RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
    },
]

# 1
app = FastAPI(
    title="Recipe API", openapi_url="/openapi.json"
)

# 2
api_router = APIRouter()


@api_router.get("/recipe/{recipe_id}", status_code=200)
def fetch_recipe(*, recipe_id: int) -> dict:  # 3
    """
    Fetch a single recipe by ID
    """

    # 4
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        return result[0]


@api_router.get("/search/", status_code=200)  # 3
def search_recipes(
    keyword: Optional[str] = None, max_results: Optional[int] = 10  # 4 & 5
) -> dict:
    """
    Search for recipes based on label keyword
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": RECIPES[:max_results]}  # 6

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)  # 7
    return {"results": list(results)[:max_results]}


# 3
@api_router.get("/", status_code=200)
def root() -> dict:
    return {"msg": "Hello, World!"}


# 4
app.include_router(api_router)

# 5
if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="localhost", port=5055, log_level="debug")
