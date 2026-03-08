from fastapi import APIRouter
from  services.fillLicense import fill_license

router = APIRouter("/license")



@router.get("")
def license_check():
    return {"status": "license"}


@router.post("/create")
def create_license():
    pass