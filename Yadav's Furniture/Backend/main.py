from auth.jwt_bearer import jwtBearer
from auth.jwt_handler import signJWT
from database import SessionLocal
from fastapi import Depends, FastAPI, HTTPException, status
from models import Admin, Bill, Client, Item
from pydantic import BaseModel
from schema import BillRequest, ClientRequest, ItemRequest, LoginRequest

app = FastAPI()

db = SessionLocal() #All Queries Comes from Here

@app.get('/clients', status_code=status.HTTP_200_OK)
def getClients():
    getClients = db.query(Client).filter().all()
    if getClients is not None:
        return getClients
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Clients are empty.")  


@app.get('/client/{client_id}',response_model=ClientRequest, status_code=status.HTTP_200_OK)
def get_client_with_id(client_id: int):
    getClient = db.query(Client).filter(Client.id == client_id).first()
    if getClient is not None:
        return getClient
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Client with this id {client_id} not found")    
        

@app.post('/client',status_code = status.HTTP_201_CREATED)
def addClient(client: ClientRequest):
    newClient = Client(
        first_name = client.first_name,
        last_name = client.last_name,
        contact_number = client.contact_number,
        address = client.address,
        description = client.description,
    )

    find_client = db.query(Client).filter(Client.contact_number == client.contact_number).first()

    if find_client != None:
        raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE, detail = "Client with this contact already exist.")

    db.add(newClient)
    db.commit()

    return {"Message":"Client Added Successfully."}

@app.put('/client/{client_id}', status_code=status.HTTP_200_OK)
def updateClient(client_id: int, client: ClientRequest):
    existing_client = db.query(Client).filter(Client.id == client_id).first()

    if not existing_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with id {client_id} not found"
        )

    existing_client.first_name = client.first_name
    existing_client.last_name = client.last_name
    existing_client.contact_number = client.contact_number
    existing_client.address = client.address
    existing_client.description = client.description

    db.commit()
    db.refresh(existing_client)

    return {"Message": "Client updated successfully", "Updated Client": existing_client}


@app.delete('/client/{client_id}', status_code=status.HTTP_200_OK)
def deleteClient(client_id: int):
    client_to_delete = db.query(Client).filter(Client.id == client_id).first()

    if not client_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with id {client_id} not found"
        )

    db.delete(client_to_delete)
    db.commit()

    return {"Message": f"Client with id {client_id} deleted successfully"}



@app.post('/login')
def login(admin:LoginRequest):
    check_admin = db.query(Admin).filter(Admin.email == admin.email and Admin.password == admin.password).first()
    if(check_admin is not None):
        return signJWT(admin.email)
    else:
        return {
            "error":"Invalid Login Details"
        }


@app.get('/items', status_code=status.HTTP_200_OK)
def getItems():
    getItems = db.query(Item).filter().all()
    if getItems is not None:
        return getItems
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Items list is empty.")  


@app.get('/item/{client_id}', status_code=status.HTTP_200_OK)
def get_items_of_specific_client(client_id: int):
    getItem = db.query(Item).filter(Item.client_id == client_id).all()
    if getItem is not None:
        return getItem
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Items for this client id {client_id} not found")    



@app.post('/item/{client_id}',status_code = status.HTTP_201_CREATED)
def addItem(item: ItemRequest):
    newItem = Item(
        client_id = item.client_id,
        name = item.name,
        size = item.size,
        quantity = item.quantity,
        price_per_piece = item.price_per_piece,
    )

    db.add(newItem)
    db.commit()

    return {"Message":"Item added successfully."}

@app.put('/item/{item_id}', status_code=status.HTTP_200_OK)
def updateItem(item_id: int, item: ItemRequest):

    existing_item = db.query(Item).filter(Item.id == item_id).first()
    if not existing_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

    existing_item.name = item.name
    existing_item.size = item.size
    existing_item.quantity = item.quantity
    existing_item.price_per_piece = item.price_per_piece

    db.commit()
    db.refresh(existing_item)

    return {"Message": "Item updated successfully", "Updated Item": existing_item}


@app.delete('/item/{item_id}', status_code=status.HTTP_200_OK)
def deleteItem(item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found."
        )
    
    db.delete(item)
    db.commit()
    
    return {"message": f"Item with id {item_id} has been deleted successfully."}

        
        
