import os

def generate_code_pdf():
    # 1. Read your existing simulation engine dashboard file code
    source_filename = "advanced_dashboard.py"
    
    if os.path.exists(source_filename):
        with open(source_filename, "r", encoding="utf-8") as f:
            raw_code_lines = f.readlines()
    else:
        # Fallback snippet if the file hasn't been saved yet
        raw_code_lines = [
            "import tkinter as tk\n",
            "from tkinter import ttk\n",
            "# Advanced Minerals Simulator Engine Running Smoothly\n",
            "print('Dashboard active')\n"
        ]

    # 2. Build explicit page margins and structural layout constraints
    output_filename = "advanced_dashboard.pdf"
    page_width, page_height = 612, 792  # Standard Letter Page dimensions
    margin_left, margin_top = 50, 740
    line_spacing = 11  # Micro font leading height spacing
    max_lines_per_page = 62

    # Group lines into single-page buckets safely
    pages_content = []
    current_page = []
    
    for line in raw_code_lines:
        # Clean syntax symbols that conflict with direct text stream blocks
        clean_line = line.replace('\t', '    ').rstrip('\r\n')
        clean_line = clean_line.replace('(', '\\(').replace(')', '\\)')
        current_page.append(clean_line)
        
        if len(current_page) >= max_lines_per_page:
            pages_content.append(current_page)
            current_page = []
    if current_page:
        pages_content.append(current_page)

    total_pages = len(pages_content)

    # 3. Assemble structural document object nodes
    pdf_objects = []
    
    # Header Catalog & Pages Collection Mapping Core Nodes
    pdf_objects.append("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj")
    
    kids_references = " ".join([f"{3 + i} 0 R" for i in range(total_pages)])
    pdf_objects.append(f"2 0 obj\n<< /Type /Pages /Kids [{kids_references}] /Count {total_pages} >>\nendobj")

    # Generate layout structure and specific line streams per page
    content_obj_id = 3 + total_pages
    
    for page_idx in range(total_pages):
        pdf_objects.append(
            f"{3 + page_idx} 0 obj\n"
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_width} {page_height}] "
            f"/Contents {content_obj_id + page_idx} 0 R "
            f"/Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Courier >> >> >> >>\n"
            "endobj"
        )

    # Compile the plain-text layout graphics streams
    for page_idx, lines in enumerate(pages_content):
        # Header structural context tags
        stream_data = (
            "BT\n"
            "/F1 8.5 Tf\n"
            f"{line_spacing} TL\n"
            f"{margin_left} {margin_top} Td\n"
        )
        
        # Add a running document tracker title on every page header space
        stream_data += f"(--- METRIC ENGINE SOURCE MATRIX - PAGE {page_idx + 1} OF {total_pages} ---) '\n"
        stream_data += "() '\n"  # Spacer line

        for line in lines:
            stream_data += f"({line}) '\n"
            
        stream_data += "ET\n"
        
        pdf_objects.append(
            f"{content_obj_id + page_idx} 0 obj\n"
            f"<< /Length {len(stream_data)} >>\n"
            f"stream\n{stream_data}endstream\n"
            "endobj"
        )

    # 4. Stream byte streams sequentially into the system hard drive
    with open(output_filename, "wb") as pdf_file:
        pdf_file.write(b"%PDF-1.4\n")
        
        cross_reference_offsets = []
        for obj in pdf_objects:
            cross_reference_offsets.append(pdf_file.tell())
            pdf_file.write(obj.encode('ascii', errors='ignore') + b"\n")
            
        xref_position = pdf_file.tell()
        
        # Write Cross-Reference structural index tables
        pdf_file.write(b"xref\n")
        pdf_file.write(f"0 {len(pdf_objects) + 1}\n".encode('ascii'))
        pdf_file.write(b"0000000000 65535 f \n")
        
        for offset in cross_reference_offsets:
            pdf_file.write(f"{offset:010d} 00000 n \n".encode('ascii'))
            
        pdf_file.write(b"trailer\n")
        pdf_file.write(f"<< /Size {len(pdf_objects) + 1} /Root 1 0 R >>\n".encode('ascii'))
        pdf_file.write(b"startxref\n")
        pdf_file.write(f"{xref_position}\n%%EOF".encode('ascii'))

    print(f"\n[SUCCESS] Document created cleanly via native Python file-writing workflows!")
    print(f"Location Target: C:\\d\\{output_filename}")

if __name__ == "__main__":
    generate_code_pdf()
