"""
Test Script for Intelligence Layer Features
Tests Memory, OCR, and PDF operations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from windows_use.agent.memory import AgentMemory
from windows_use.agent.tools.service import memory_operation_tool, ocr_tool, pdf_operation_tool
from windows_use.desktop import Desktop

print("=" * 60)
print("🧠 INTELLIGENCE LAYER TEST SUITE")
print("=" * 60)
print()

desktop = Desktop()

# Test 1: Memory Operations
print("📋 TEST 1: Memory Operations")
print("-" * 60)

print("\n1. Save a template...")
result = memory_operation_tool(
    operation='save_template',
    template_name='test_workflow',
    command='Take screenshot and save as test',
    description='Test workflow for demonstration',
    desktop=desktop
)
print(result)

print("\n2. List all templates...")
result = memory_operation_tool(
    operation='list_templates',
    desktop=desktop
)
print(result)

print("\n3. Load the template...")
result = memory_operation_tool(
    operation='load_template',
    template_name='test_workflow',
    desktop=desktop
)
print(result)

print("\n4. Get memory statistics...")
result = memory_operation_tool(
    operation='statistics',
    desktop=desktop
)
print(result)

# Test 2: Add some command history
print("\n\n📜 TEST 2: Command History")
print("-" * 60)

memory = AgentMemory()
memory.add_command("Take screenshot", "✅ Screenshot saved", ["screenshot_tool"])
memory.add_command("Calculate 100+200", "✅ Result: 300", ["calculate_tool"])
memory.add_command("Open Chrome", "✅ Chrome launched", ["launch_tool"])

print("\n1. View recent history...")
result = memory_operation_tool(
    operation='recent_history',
    count=5,
    desktop=desktop
)
print(result)

print("\n2. Search history for 'screenshot'...")
result = memory_operation_tool(
    operation='search_history',
    search_query='screenshot',
    count=3,
    desktop=desktop
)
print(result)

# Test 3: OCR (requires image)
print("\n\n👁️ TEST 3: OCR Tool")
print("-" * 60)
print("Note: OCR requires pytesseract and Tesseract-OCR installed")
print("      and an image file to test with")

# Check if sample image exists
test_image_path = os.path.join(os.path.expanduser("~"), "Desktop", "test_image.png")
if os.path.exists(test_image_path):
    print(f"\n1. Extract text from {test_image_path}...")
    result = ocr_tool(image_path=test_image_path, desktop=desktop)
    print(result)
else:
    print(f"\n⚠️ No test image found at {test_image_path}")
    print("   Create an image with text to test OCR functionality")

# Test 4: PDF Operations (requires PDF files)
print("\n\n📄 TEST 4: PDF Operations")
print("-" * 60)
print("Note: PDF operations require PyPDF2 installed")
print("      and PDF files to test with")

# Check if sample PDFs exist
test_pdf1 = os.path.join(os.path.expanduser("~"), "Desktop", "test1.pdf")
test_pdf2 = os.path.join(os.path.expanduser("~"), "Desktop", "test2.pdf")
output_pdf = os.path.join(os.path.expanduser("~"), "Desktop", "merged_test.pdf")

if os.path.exists(test_pdf1) and os.path.exists(test_pdf2):
    print(f"\n1. Merge {test_pdf1} and {test_pdf2}...")
    result = pdf_operation_tool(
        operation='merge',
        input_files=[test_pdf1, test_pdf2],
        output_file=output_pdf,
        desktop=desktop
    )
    print(result)
else:
    print(f"\n⚠️ No test PDFs found")
    print("   Create test1.pdf and test2.pdf on Desktop to test PDF merge")

# Extract text from PDF
if os.path.exists(test_pdf1):
    output_txt = os.path.join(os.path.expanduser("~"), "Desktop", "extracted_text.txt")
    print(f"\n2. Extract text from {test_pdf1}...")
    result = pdf_operation_tool(
        operation='extract_text',
        input_files=[test_pdf1],
        output_file=output_txt,
        desktop=desktop
    )
    print(result)

# Summary
print("\n\n" + "=" * 60)
print("✅ TEST SUITE COMPLETE")
print("=" * 60)
print()
print("📊 Summary:")
print("   • Memory operations: ✅ Tested")
print("   • Command history: ✅ Tested")
print("   • Template workflows: ✅ Tested")
print("   • OCR: ⚠️ Requires image file")
print("   • PDF operations: ⚠️ Requires PDF files")
print()
print("💡 Next Steps:")
print("   1. Install dependencies: install_intelligence_layer.bat")
print("   2. Create test images and PDFs")
print("   3. Run full integration tests")
print()
print("🎯 Memory Data Location:")
print(f"   {os.path.join(os.path.expanduser('~'), 'Documents', 'PowerAgent', 'Memory')}")
print()
