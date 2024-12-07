from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_current_user():
    # TODO: Implement get current user
    pass

@router.put("/me")
def update_user():
    # TODO: Implement update user
    pass