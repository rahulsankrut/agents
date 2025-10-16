# 🎯 FedEx Site Selection Intelligence Demo
## Helping Businesses Find Their Next Winning Location

---

## ⚡ Quick Start

**Best Demo Options (by data richness):**

1. **🥇 Petco Demo** - `pet_shop` category (RECOMMENDED)
2. **🥈 Best Buy Demo** - `electronics` category (EXCELLENT)  
3. **🥉 Sephora Demo** - `health_beauty` category (GREAT)
4. **Starbucks Demo** - `drinks` category (LIMITED DATA)

**Why?** Categories with more products = more zip codes = better visualizations!

---

## 📖 Demo Story Arc

This demo tells the story of how **Starbucks** uses FedEx shipment intelligence to identify optimal locations for new stores.

### The Journey:
```
Market Discovery → Growth Analysis → Regional Focus → City Comparison → Neighborhood Pinpointing → Final Recommendation
```

---

## 🎬 How to Run the Demo

### Option 1: Full Narrative Demo (Recommended for Presentations)
```bash
cd /Users/rahulkasanagottu/Desktop/agents/fedex
source ../venv/bin/activate
python starbucks_demo.py
```

**Best for:** 
- Live customer presentations
- Executive demos
- Sales meetings
- Investor presentations

**Duration:** 10-15 minutes

---

### Option 2: Interactive Web UI
```bash
cd /Users/rahulkasanagottu/Desktop/agents/fedex
source ../venv/bin/activate
adk web
```

**Best for:**
- Hands-on customer workshops
- Technical demos
- POC sessions
- Custom queries

---

## 📊 The 6-Phase Demo Story

### **Phase 1: Market Discovery** 🔍
**Business Question:** *"What market opportunities exist?"*

**Query:** 
```
"What product categories are available in the dataset?"
```

**Insight:** Understand the breadth of data and identify relevant categories for Starbucks (food, beverages, etc.)

**Customer Value:** Know what intelligence is available before diving deep

---

### **Phase 2: Growth Analysis** 📈
**Business Question:** *"Where is demand growing fastest?"*

**Query:** 
```
"Show me cities with the highest growth in drinks shipments"
```

**Insight:** Identify emerging markets with momentum, not just large existing markets

**Customer Value:** Get ahead of competitors by spotting trends early

**Expected Output:**
- Growth rate percentages by city (e.g., New York: 75%, Washington DC: 67%)
- Visualization of top growing markets
- Early vs. recent period comparison

**Actual Results:**
- New York, NY: 75% growth
- Washington, DC: 67% growth  
- Los Angeles, CA: 33% growth

---

### **Phase 3: State-Level Analysis** 🎯
**Business Question:** *"Which state/region should we prioritize?"*

**Query:** 
```
"Analyze drinks demand in California. Show me the top 10 cities."
```

**Insight:** Deep dive into a specific state to understand market saturation and opportunities

**Customer Value:** State-level rollout strategy with data-backed prioritization

**Expected Output:**
- Heatmap of demand by city
- Shipment volumes and customer counts
- Revenue potential estimates

**Actual Results:**
- Los Angeles leads California with highest drinks shipments
- Multiple cities showing demand across the state

---

### **Phase 4: City Comparison** ⚖️
**Business Question:** *"Los Angeles or San Diego - which city first?"*

**Query:** 
```
"Compare drinks shipment volumes between Los Angeles, CA and San Diego, CA"
```

**Insight:** Objective comparison between expansion candidates

**Customer Value:** Remove guesswork from location prioritization

**Expected Output:**
- Side-by-side metrics comparison
- Clear winner recommendation
- Supporting data (volume, recipients, revenue)

**Actual Results:**
- **Los Angeles**: 12 shipments, $727.60 revenue
- **San Diego**: 3 shipments, $416.29 revenue (higher avg value)
- Winner: Los Angeles for volume, San Diego for premium customers

---

### **Phase 5: Neighborhood Pinpointing** 📍
**Business Question:** *"Where exactly should we open stores?"*

**Query:** 
```
"Use the identify_demand_gaps function to find high-demand underserved areas 
for drinks in California. Show me the top zip codes."
```

**Insight:** Specific neighborhoods with high demand and potential gaps

**Customer Value:** Street-level precision for site selection

**Expected Output:**
- Top zip codes ranked by demand score
- Customer density metrics
- Visual demand gap analysis
- Revenue opportunity sizing

**Note:** For categories with limited data (like drinks), consider using high-volume categories like:
- `pet_shop` (for Petco demo) - 100+ zip codes
- `electronics` (for Best Buy demo) - 1,000+ zip codes
- `health_beauty` (for Sephora demo) - 2,000+ products

---

### **Phase 6: Final Recommendation** 🏆
**Business Question:** *"What's our action plan?"*

**Deliverable:** Executive summary with:
- ✅ Top 3 recommended locations
- ✅ Data-backed reasoning for each
- ✅ Revenue potential estimates
- ✅ Risk assessment
- ✅ Next steps roadmap

**Customer Value:** Actionable, board-ready recommendations

---

## 💡 Demo Tips & Talk Track

### Opening Hook (2 minutes)
```
"Starbucks opens hundreds of stores every year. But how do you know 
WHERE to open them? Traditionally, it's been a mix of gut feel, 
demographics, and foot traffic studies. 

But what if you could see ACTUAL CONSUMER BEHAVIOR? What if you knew 
where people are already ordering coffee and beverages - before you 
ever open a store?

That's the power of FedEx shipment intelligence. Let me show you..."
```

### During the Demo
- **Pause** after each phase for questions
- **Highlight** the progression from broad to specific
- **Emphasize** the data-driven nature (no guessing)
- **Show** visualizations prominently
- **Connect** each insight to business value

### Key Messages to Reinforce
1. **Actual Behavior** - Shipment data = what people actually buy, not surveys
2. **Leading Indicator** - See demand before competitors do
3. **Risk Reduction** - Data-backed decisions reduce new store failures
4. **Scalable** - Same process for any city, any product
5. **Competitive Edge** - Intelligence your competitors don't have

---

## 🎯 Customer-Specific Variations

### For Starbucks
- **Categories:** `drinks`, `food_drink`, `food`
- **Best States:** California, New York, Texas
- **Regions:** Urban areas, college towns, suburban growth
- **Note:** Drinks has limited data; consider using `food_drink` for richer analysis

### For Petco (RECOMMENDED - Best data coverage)
- **Category:** `pet_shop`
- **Best States:** California, Texas, Florida, Arizona
- **Regions:** Suburban family neighborhoods
- **Why:** Excellent data volume, clear demand patterns

### For Best Buy (RECOMMENDED - Rich data)
- **Categories:** `electronics`, `computers`, `computers_accessories`, `telephony`
- **Best States:** California, Texas, New York, Washington
- **Regions:** Tech-heavy metros, high-income areas
- **Why:** 1,600+ products, excellent geographic coverage

### For Chipotle
- Focus on: food, meal delivery
- Regions: Urban lunch zones, college campuses
- Competition: Fast-casual density gaps

---

## 📈 Expected Results by Phase

| Phase | Time | Key Deliverable |
|-------|------|----------------|
| 1. Market Discovery | 1 min | Category overview (drinks, food_drink, food) |
| 2. Growth Analysis | 2 min | Top growing cities (NY: 75%, DC: 67%) |
| 3. State Analysis | 2 min | California city rankings (LA leads) |
| 4. City Comparison | 2 min | Los Angeles vs San Diego metrics |
| 5. Neighborhood Pinpoint | 3 min | High-demand zip codes in target city |
| 6. Recommendation | 3 min | Executive summary with actionable insights |

**Total:** 13-15 minutes

**Note:** For more impressive demos with richer data, use high-volume categories:
- `pet_shop` for Petco (better zip code coverage)
- `electronics` or `computers` for Best Buy (1,000+ products)
- `health_beauty` for Sephora (2,400+ products)
- `sports_leisure` for Dick's Sporting Goods (2,800+ products)

---

## 🚀 Call to Action

### After the Demo
```
"What you've seen today is just one use case. This same intelligence 
can help you:

✓ Prioritize international expansion
✓ Optimize delivery center locations  
✓ Plan seasonal pop-up locations
✓ Identify acquisition targets
✓ Forecast demand for new products

The question isn't whether to use shipment intelligence - it's how 
fast can you deploy it before your competitors do?

Let's discuss next steps for a pilot in your expansion planning..."
```

---

## 📞 Next Steps

1. **Pilot Program**: Test on 3 planned locations
2. **ROI Analysis**: Compare agent recommendations vs traditional methods
3. **Integration**: Connect to your existing site selection tools
4. **Expansion**: Roll out to all regional planners

---

## 🎁 Bonus Queries for Q&A

If customers ask for more, try these **working queries**:

```
"Show me cities with highest growth in pet_shop shipments"

"Analyze electronics demand in Texas. Show me the top cities."

"Compare pet_shop shipment volumes between Phoenix, AZ and Tampa, FL"

"Identify high-demand areas for health_beauty in California"

"What are the top 10 zip codes nationwide for sports_leisure products?"

"Show me furniture_decor demand across major cities"
```

**Pro Tip:** Use categories with rich data for best results:
- `pet_shop`, `electronics`, `health_beauty`, `sports_leisure`, `furniture_decor`

---

## ✅ Success Metrics

**A successful demo achieves:**
- [ ] Customer says "wow" at least twice
- [ ] Customer asks "can we see our data?"
- [ ] Customer requests specific city analysis
- [ ] Customer schedules follow-up meeting
- [ ] Customer asks about pricing/timeline

---

**Demo Created:** October 2025  
**Last Updated:** October 2025  
**Version:** 1.0 - Starbucks Narrative Demo

