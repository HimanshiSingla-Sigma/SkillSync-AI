from fastapi import HTTPException, status


class CareerConnectException(HTTPException):
    """Base application exception."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(CareerConnectException):
    def __init__(self, detail: str = "Resource not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestException(CareerConnectException):
    def __init__(self, detail: str = "Bad request parameters."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedException(CareerConnectException):
    def __init__(self, detail: str = "Invalid credentials or unauthorized token."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class ForbiddenException(CareerConnectException):
    def __init__(self, detail: str = "Access forbidden. Insufficient permissions."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ConflictException(CareerConnectException):
    def __init__(self, detail: str = "Resource conflict. Duplicate entry."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class AIInferenceException(CareerConnectException):
    def __init__(self, detail: str = "AI Inference or GraphRAG service error."):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail
        )