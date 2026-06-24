FROM python:3.12

# Create a non-root user for Hugging Face Spaces compatibility
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Install dependencies
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=user . /app

# Run database migrations, run seed script, and run the Django dev server on port 7860
CMD python manage.py migrate && python setup.py && python manage.py runserver 0.0.0.0:7860
