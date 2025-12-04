from fastapi import FastAPI
from api.decrypt_seed_endpoint import router as decrypt_router
from api.generate_2fa_endpoint import router as generate_2fa_router
from api.verify_2fa import router as verify_router

app = FastAPI()

# Register the endpoint
app.include_router(decrypt_router)
app.include_router(generate_2fa_router)
app.include_router(verify_router)
