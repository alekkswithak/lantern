from fastapi import FastAPI, Depends
from src.dependencies import get_data_repository, get_pdf_service
from src.pdf_service import PdfService
from src.data_repository import DataRepository
from src.schemas import DataComparisonRequest, DataComparisonResponse
from src.helpers import compare_data

app = FastAPI()


@app.post("/", response_model=DataComparisonResponse)
def post_data_comparison(
    request: DataComparisonRequest,
    pdf_service: PdfService = Depends(get_pdf_service),
    data_repository: DataRepository = Depends(get_data_repository),
):
    """
    Perform a comparison between data extracted from a PDF file and data retrieved from a database.

    Args:
        request (DataComparisonRequest): The request containing file path and company name.
        pdf_service (PdfService, optional): The PDF service dependency.
        data_repository (DataRepository, optional): The data repository dependency.

    Returns:
        DataComparisonResponse: A response containing the comparison results including the company name,
        file data, database data, and differences between them.
    """
    file_data = pdf_service.extract(file_path=request.filepath)
    db_data = data_repository.get_company_data(request.company_name)

    differences = compare_data(file_data, db_data)

    response = DataComparisonResponse(
        company_name=request.company_name,
        file_data=file_data,
        db_data=db_data,
        differences=differences,
    )

    return response
