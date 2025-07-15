import logging
from pydantic import BaseModel, field_validator, Field
from typing import Optional, Union
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

class BookDetails(BaseModel):
    """
    Book details model for OpenLibrary API response.
    
    Represents individual book information from the OpenLibrary search results.
    """

    author_name: Optional[str] = Field(
        None, 
        description="Name of the book's author"
    )
    edition_count: Optional[int] = Field(
        None, 
        ge=0, 
        description="Number of editions available for this book"
    )
    first_publish_year: Optional[int] = Field(
        None, 
        ge=1000, 
        le=datetime.now().year + 1,
        description="Year the book was first published"
    )
    language: Optional[Union[str, list[str]]] = Field(
        None, 
        description="Language(s) of the book"
    )
    title: Optional[str] = Field(
        None, 
        description="Title of the book"
    )
    
    @field_validator("author_name", mode="before")
    def validate_author_fields(cls, v):
        """
        Validate author fields by extracting first element if it's a list.
        
        Args:
            v: The value to validate (can be str, list, or None)
            
        Returns:
            str or None: The validated author field value
        """
        if v is None:
            return None
        
        if isinstance(v, list):
            if len(v) > 0:
                logger.debug(f"📝 Author validation: Converting list {v} to first element: '{v[0]}'")
                return v[0]
            else:
                logger.debug("📝 Author validation: Empty list provided, returning None")
                return None
        
        logger.debug(f"📝 Author validation: Using string value: '{v}'")
        return v
    
    @field_validator("language", mode="before")
    def validate_language(cls, v):
        """
        Validate language field by normalizing it to a consistent format.
        
        Args:
            v: The value to validate (can be str, list, or None)
            
        Returns:
            str or None: The primary language if multiple languages are provided
        """
        if v is None:
            return None
            
        if isinstance(v, list):
            if len(v) > 0:
                logger.debug(f"🌍 Language validation: Multiple languages {v}, using primary: '{v[0]}'")
                return v[0]  # Return primary language
            else:
                logger.debug("🌍 Language validation: Empty language list provided")
                return None
        
        logger.debug(f"🌍 Language validation: Using single language: '{v}'")
        return v
    
    @field_validator("title", mode="before")
    def validate_title(cls, v):
        """
        Validate and clean title field.
        
        Args:
            v: The title value to validate
            
        Returns:
            str or None: The cleaned title
        """
        if v is None:
            return None
            
        if isinstance(v, str):
            cleaned = v.strip()
            if cleaned != v:
                logger.debug(f"📖 Title validation: Cleaned whitespace from '{v}' to '{cleaned}'")
            return cleaned
        
        # Convert non-string to string if not None
        if v:
            result = str(v)
            logger.debug(f"📖 Title validation: Converted {type(v).__name__} to string: '{result}'")
            return result
        
        return None


class OpenLibrary(BaseModel):
    """
    OpenLibrary API response model.
    
    Represents the complete response from OpenLibrary search API.
    """
    
    num_found: int = Field(
        description="Total number of books found in the search"
    )
    q: str = Field(
        description="The search query that was executed"
    )
    docs: list[BookDetails] = Field(
        description="List of book details from the search results"
    )
    
    def __init__(self, **data):
        """Initialize OpenLibrary model with logging"""
        logger.debug(f"🏗️  Creating OpenLibrary model with {len(data.get('docs', []))} book records")
        
        # Track validation issues
        docs_data = data.get('docs', [])
        if docs_data:
            incomplete_books = 0
            for doc in docs_data:
                required_fields = ['title', 'author_name']
                missing_fields = [field for field in required_fields if not doc.get(field)]
                if missing_fields:
                    incomplete_books += 1
            
            if incomplete_books > 0:
                logger.info(f"⚠️  {incomplete_books}/{len(docs_data)} books have missing critical fields")
        
        super().__init__(**data)
        
        # Log successful creation
        logger.debug(f"✅ OpenLibrary model created successfully: {self.num_found} total, {len(self.docs)} processed")
    
    class Config:
        """Pydantic model configuration."""
        # Allow extra fields from API response that we don't explicitly model
        extra = "ignore"
        # Validate field defaults
        validate_default = True
