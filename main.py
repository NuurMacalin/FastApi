from data import menu_items
from models import MenuItem, MenuResponse  # Moodaladii aad soo qortay
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

@app.get("/menu", response_model=MenuResponse)
def get_menu(category: str | None = None):
    # 1. Haddii uu jiro shaandhayn (filter) category ah
    if category:
        filters = [item for item in menu_items if item["category"].lower() == category.lower()]

        if not filters:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"No menu items found in category: {category}"
            )
        # Halkan waxaa si otomaatig ah ugu darmaya status="success" mar haddii model-ka lagu sii qeexay
        return MenuResponse(count=len(filters), items=filters)

    # 2. Haddii la rabo dhammaan menu-ka
    return MenuResponse(count=len(menu_items), items=menu_items)


@app.get("/menu/{item_id}", response_model=MenuItem)

def get_menu_item(item_id: int):
    for item in menu_items:
        if item["id"] == item_id:
            return item
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,)
