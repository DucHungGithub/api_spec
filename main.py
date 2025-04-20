import os
from functools import partial

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import uvicorn

from routers import OutletRouter, PromotionRouter, ImageRouter, LocationRouter, StaffRouter



def custom_openapi(app: FastAPI):
    if not app.openapi_schema:
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        openapi_schema["components"]["schemas"].update(
            {
                "HTTPError": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "error": {"type": "string"},
                        "details": {"type": "string"},
                        "server_date_time": {"type": "string"},
                    },
                },
                "InternalServerError": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "error": {"type": "string"},
                        "server_date_time": {"type": "string"},
                    },
                },
            }
        )

        # Define common error responses
        common_responses = {
            "400": {
                "description": "Bad Request",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/HTTPError"},
                        "example": {
                            "name": "Service Exception",
                            "error": "PLANOGRAM_REQUEST_BODY_INVALID",
                            "details": "Request body is invalid",
                            "server_date_time": "2025-01-17T14:00:11.647441+00:00",
                        },
                    }
                },
            },
            "401": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/HTTPError"},
                        "example": {
                            "name": "Unauthorized Exception",
                            "error": "UNAUTHORIZED",
                            "details": "Unauthorized",
                            "server_date_time": "2025-01-17T14:00:11.647441+00:00",
                        },
                    }
                },
            },
            "403": {
                "description": "Forbidden",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/HTTPError"},
                        "example": {
                            "name": "Forbidden Exception",
                            "error": "FORBIDDEN",
                            "details": "Forbidden",
                            "server_date_time": "2025-01-17T14:00:11.647441+00:00",
                        },
                    }
                },
            },
            "404": {
                "description": "Not Found",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/HTTPError"},
                        "example": {
                            "name": "Not Found Exception",
                            "error": "NOT_FOUND",
                            "details": "Not Found",
                            "server_date_time": "2025-01-17T14:00:11.647441+00:00",
                        },
                    }
                },
            },
            "500": {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/InternalServerError"},
                        "example": {
                            "name": "Internal Server Error",
                            "error": "INTERNAL_SERVER_ERROR",
                            "server_date_time": "2025-01-17T14:00:11.647441+00:00",
                        },
                    },
                },
            },
        }
        for _, method_item in openapi_schema.get("paths").items():  # type: ignore
            for _, param in method_item.items():
                responses = param.get("responses")
                # remove 422 response, also can remove other status code
                if "422" in responses:
                    del responses["422"]

        # Add responses to all paths
        for path in openapi_schema["paths"].values():
            for operation in path.values():
                if "responses" not in operation:
                    operation["responses"] = {}
                operation["responses"].update(common_responses)

        app.openapi_schema = openapi_schema
    return app.openapi_schema



app = FastAPI()

app.include_router(OutletRouter(), prefix="/outlets", tags=["Outlets"])
app.include_router(PromotionRouter(), prefix="/promotions", tags=["Promotions"])
app.include_router(LocationRouter(), prefix="/locations", tags=["Locations"])
app.include_router(StaffRouter(), prefix="/staffs", tags=["Staffs"])
app.include_router(ImageRouter(), tags=["Images"])

app.openapi = partial(custom_openapi, app)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))