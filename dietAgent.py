
# I will get the dishname and the quantity like rice 100gm
# a system for calculating calories
# a system for segrigating curbs,fat and porteen
# a system for calculating calories
# a system to generate the diet in structure
# a system to send the diet chart to whatsaap

from flask import Flask, request, jsonify
import json
from fpdf import FPDF
from twilio.rest import Client
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Mock database for nutritional values
nutrition_db = {
    "rice": {"calories": 130, "carbs": 28, "protein": 2.7, "fat": 0.3, "fiber": 0.4},
    "chicken": {"calories": 239, "carbs": 0, "protein": 27, "fat": 14, "fiber": 0},
    "dal": {"calories": 116, "carbs": 20, "protein": 9, "fat": 0.4, "fiber": 7.9},
    "fish": {"calories": 97, "carbs": 0, "protein": 21, "fat": 1.5, "fiber": 0},
    "mustard oil": {"calories": 884, "carbs": 0, "protein": 0, "fat": 100, "fiber": 0},
    "potato": {"calories": 77, "carbs": 17, "protein": 2, "fat": 0.1, "fiber": 2.2},
    "brinjal (eggplant)": {"calories": 25, "carbs": 6, "protein": 1, "fat": 0.2, "fiber": 3},
    "hilsa fish": {"calories": 190, "carbs": 0, "protein": 22, "fat": 11, "fiber": 0},
    "panta bhaat": {"calories": 162, "carbs": 35, "protein": 2.5, "fat": 0.5, "fiber": 1},
    "shorshe ilish": {"calories": 260, "carbs": 3, "protein": 22, "fat": 18, "fiber": 1},
    "luchi": {"calories": 150, "carbs": 16, "protein": 2, "fat": 9, "fiber": 0.5},
    "aloo posto": {"calories": 180, "carbs": 14, "protein": 4, "fat": 12, "fiber": 3},
    "rosogolla": {"calories": 140, "carbs": 33, "protein": 2.1, "fat": 0.1, "fiber": 0},
    "sandesh": {"calories": 150, "carbs": 25, "protein": 4, "fat": 5, "fiber": 0},
    "cholar dal": {"calories": 133, "carbs": 22, "protein": 9, "fat": 2.3, "fiber": 5.1},
    "mishti doi": {"calories": 120, "carbs": 18, "protein": 4, "fat": 4, "fiber": 0},
    "shorshe bata maach": {"calories": 220, "carbs": 5, "protein": 22, "fat": 14, "fiber": 1},
    "muri": {"calories": 380, "carbs": 85, "protein": 7, "fat": 2.6, "fiber": 4},
    "beguni": {"calories": 150, "carbs": 16, "protein": 1.5, "fat": 9.5, "fiber": 2},
    "khichuri": {"calories": 180, "carbs": 36, "protein": 4, "fat": 2, "fiber": 1.5},
    "payesh": {"calories": 120, "carbs": 22, "protein": 3, "fat": 4, "fiber": 0},
    "biryani": {"calories": 160, "carbs": 28, "protein": 5, "fat": 6, "fiber": 1.5},
    "kachaudi": {"calories": 250, "carbs": 30, "protein": 5, "fat": 12, "fiber": 1},
    "shorshe chutney": {"calories": 120, "carbs": 20, "protein": 1.5, "fat": 4, "fiber": 1},
    "chicken curry": {"calories": 234, "carbs": 4, "protein": 25, "fat": 14, "fiber": 0},
    "aloo paratha": {"calories": 250, "carbs": 34, "protein": 5, "fat": 10, "fiber": 3},
    "samosa": {"calories": 200, "carbs": 26, "protein": 3, "fat": 10, "fiber": 2},
    "puri": {"calories": 210, "carbs": 26, "protein": 3, "fat": 12, "fiber": 1.5},
    "prawn malai curry": {"calories": 250, "carbs": 8, "protein": 22, "fat": 15, "fiber": 1},
    "macher jhol": {"calories": 180, "carbs": 5, "protein": 20, "fat": 8, "fiber": 0},
    "tandoori chicken": {"calories": 195, "carbs": 4, "protein": 30, "fat": 8, "fiber": 1},
    "chapati": {"calories": 120, "carbs": 25, "protein": 3, "fat": 0.5, "fiber": 2.5},
    "dal makhani": {"calories": 230, "carbs": 25, "protein": 9, "fat": 9, "fiber": 6},
    "malai kofta": {"calories": 310, "carbs": 18, "protein": 8, "fat": 22, "fiber": 2},
    "chana masala": {"calories": 160, "carbs": 27, "protein": 8, "fat": 4, "fiber": 8},
    "aloo gobi": {"calories": 130, "carbs": 22, "protein": 3, "fat": 4, "fiber": 4},
    "baingan bharta": {"calories": 120, "carbs": 24, "protein": 3, "fat": 5, "fiber": 8},
    "dosa": {"calories": 150, "carbs": 30, "protein": 3, "fat": 4, "fiber": 1},
    "idli": {"calories": 80, "carbs": 15, "protein": 2, "fat": 1, "fiber": 0.5},
    "vada": {"calories": 190, "carbs": 25, "protein": 5, "fat": 8, "fiber": 2},
    "paratha": {"calories": 200, "carbs": 30, "protein": 5, "fat": 8, "fiber": 3},
    "pav bhaji": {"calories": 250, "carbs": 45, "protein": 6, "fat": 8, "fiber": 7},
    "bhel puri": {"calories": 200, "carbs": 40, "protein": 4, "fat": 6, "fiber": 2},
    "pani puri": {"calories": 150, "carbs": 30, "protein": 4, "fat": 5, "fiber": 1},
    "chole bhature": {"calories": 350, "carbs": 50, "protein": 10, "fat": 14, "fiber": 3},
    "dhokla": {"calories": 140, "carbs": 24, "protein": 4, "fat": 3, "fiber": 2},
    "kadhi pakora": {"calories": 220, "carbs": 20, "protein": 6, "fat": 14, "fiber": 4},
    "pulao": {"calories": 150, "carbs": 30, "protein": 4, "fat": 5, "fiber": 1},
    "vegetable biryani": {"calories": 180, "carbs": 35, "protein": 5, "fat": 7, "fiber": 2},
    "tikka masala": {"calories": 200, "carbs": 10, "protein": 18, "fat": 12, "fiber": 2},
    "butter chicken": {"calories": 400, "carbs": 10, "protein": 20, "fat": 28, "fiber": 1},
    "prawn curry": {"calories": 220, "carbs": 6, "protein": 22, "fat": 12, "fiber": 1},
    "gobi manchurian": {"calories": 250, "carbs": 20, "protein": 5, "fat": 18, "fiber": 4},
    "vegetable kofta": {"calories": 270, "carbs": 20, "protein": 6, "fat": 18, "fiber": 5},
    "korma": {"calories": 320, "carbs": 15, "protein": 8, "fat": 22, "fiber": 2},
    "roti": {"calories": 150, "carbs": 30, "protein": 4, "fat": 1, "fiber": 3},
    "kulfi": {"calories": 280, "carbs": 35, "protein": 5, "fat": 12, "fiber": 0},
    "sewai": {"calories": 180, "carbs": 35, "protein": 4, "fat": 6, "fiber": 1},
    "gajar halwa": {"calories": 120, "carbs": 20, "protein": 2, "fat": 5, "fiber": 2},
    "badam halwa": {"calories": 350, "carbs": 40, "protein": 8, "fat": 18, "fiber": 3},
    "raita": {"calories": 110, "carbs": 8, "protein": 5, "fat": 8, "fiber": 1},
    "kheer": {"calories": 180, "carbs": 30, "protein": 6, "fat": 6, "fiber": 1},
    "laal maas": {"calories": 300, "carbs": 10, "protein": 25, "fat": 18, "fiber": 2},
    "patra": {"calories": 130, "carbs": 25, "protein": 5, "fat": 4, "fiber": 2},
    "sindhi biryani": {"calories": 210, "carbs": 45, "protein": 6, "fat": 9, "fiber": 2},
    "batata vada": {"calories": 140, "carbs": 25, "protein": 3, "fat": 4, "fiber": 2},
    "pav": {"calories": 270, "carbs": 50, "protein": 7, "fat": 5, "fiber": 3},
    "idli sambhar": {"calories": 200, "carbs": 40, "protein": 8, "fat": 3, "fiber": 4},
}


# AI agent to fetch nutritional info
def ai_fetch_nutrition(dish_name):
    if dish_name in nutrition_db:
        return nutrition_db[dish_name]
    # Simulate AI agent fetching data
    return {"calories": 100, "carbs": 10, "protein": 5, "fat": 2, "fiber": 1}

# Route to get nutrition info
@app.route("/api/nutrition", methods=["POST"])
def get_nutrition():
    data = request.json
    dish_name = data.get("dishName").lower()
    quantity = data.get("quantity", 100)

    nutrition = ai_fetch_nutrition(dish_name)
    if not nutrition:
        return jsonify({"error": "Dish not found"}), 404

    # Scale nutrition by quantity
    scaled_nutrition = {k: v * (quantity / 100) for k, v in nutrition.items()}
    return jsonify(scaled_nutrition)

# Route to generate PDF and send via WhatsApp
@app.route("/api/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.json
    sections = data.get("sections")
    target_calories = data.get("targetCalories")
    tracked_calories = data.get("trackedCalories")
    whatsapp_number = data.get("whatsappNumber")

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Diet Chart", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Target Calories: {target_calories}", ln=True)
    pdf.cell(200, 10, txt=f"Tracked Calories: {tracked_calories}", ln=True)

    for section, items in sections.items():
        pdf.cell(200, 10, txt=section.title(), ln=True)
        for item in items:
            text = f"{item['dishName']} ({item['quantity']}g): {item['calories']} kcal"
            pdf.cell(200, 10, txt=text, ln=True)

    pdf_file = "diet_chart.pdf"
    pdf.output(pdf_file)

    # Send via WhatsApp (using Twilio)
    client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")
    message = client.messages.create(
        from_="whatsapp:+918910818207",
        body="Your diet chart is ready. Please find the attached PDF.",
        to=f"whatsapp:{whatsapp_number}",
    )

    with open(pdf_file, "rb") as f:
        client.messages.create(
            from_="whatsapp:+918910818207",
            media_url=f"https://example.com/{pdf_file}",
            to=f"whatsapp:{whatsapp_number}",
        )

    return jsonify({"message": "PDF generated and sent via WhatsApp"})

if __name__ == "__main__":
    app.run(debug=True)
