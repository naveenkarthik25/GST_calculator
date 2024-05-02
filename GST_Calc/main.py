from fastapi import FastAPI

app = FastAPI()

# Dataset of products with their GST rates
products = [
    {"name": "Milk", "gst_rate_percent": 5},
    {"name": "Bread", "gst_rate_percent": 12},
    {"name": "Soap", "gst_rate_percent": 18}
]

def calculate_gst(amount, gst_rate):
    cgst_rate = gst_rate / 2
    sgst_rate = gst_rate / 2
    igst_rate = gst_rate

    cgst = (amount * cgst_rate) / 100
    sgst = (amount * sgst_rate) / 100
    utgst = sgst  # UTGST is same as SGST in this case
    igst = (amount * igst_rate) / 100

    return cgst, sgst, utgst, igst

def calculate_amount_including_gst(amount, gst_rate):
    cgst, sgst, _, _ = calculate_gst(amount, gst_rate)
    total_gst = cgst + sgst
    return amount + total_gst

def calculate_gst_details(amount, gst_rate):
    cgst, sgst, utgst, igst = calculate_gst(amount, gst_rate)
    return cgst, sgst, utgst, igst

@app.post("/calculate_gst/")
async def calculate_gst_endpoint(product_name: str, amount: float):
    gst_rate_percent = None
    
    # Check if product exists in the dataset
    for product in products:
        if product["name"] == product_name:
            gst_rate_percent = product["gst_rate_percent"]
            break

    if gst_rate_percent is None:
        # If product not found in dataset, calculate GST manually
        cgst, sgst, utgst, igst = calculate_gst_details(amount, 18)  # Assuming 18% GST if product not found
        gst_rate_percent = 18
    else:
        cgst, sgst, utgst, igst = calculate_gst_details(amount, gst_rate_percent)

    amount_including_gst = calculate_amount_including_gst(amount, gst_rate_percent)
    
    return {
        "Product_Name": product_name,
        "CGST": cgst,
        "SGST": sgst,
        "UTGST": utgst,
        "IGST": igst,
        "Amount_excluding_GST": amount,
        "Amount_including_GST": amount_including_gst,
        "GST": igst if cgst == sgst else cgst + sgst
    }
