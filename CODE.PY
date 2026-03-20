# ============================================
# 📦 1. IMPORT LIBRARIES
# ============================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================
# 📂 2. LOAD DATASET
# ============================================

# IMPORTANT: use separator ';'
df = pd.read_csv('bank-full.csv', sep=';')

print("Shape:", df.shape)
df.head()

# ============================================
# 🧹 3. DATA CLEANING
# ============================================

# Check missing values
print(df.isnull().sum())

# Convert target column to binary
df['y'] = df['y'].map({'yes': 1, 'no': 0})

print(df['y'].value_counts())


# ============================================
# 📊 4. FUNNEL CREATION
# ============================================

total_contacts = len(df)

# Leads = people who were successfully contacted (duration > 0)
leads = df[df['duration'] > 0].shape[0]

# Customers = subscribed
customers = df[df['y'] == 1].shape[0]

funnel = pd.DataFrame({
    'Stage': ['Contacts', 'Leads', 'Customers'],
    'Count': [total_contacts, leads, customers]
})

funnel

# ============================================
# 📈 5. CONVERSION RATES
# ============================================

contact_to_lead = (leads / total_contacts) * 100
lead_to_customer = (customers / leads) * 100
overall_conversion = (customers / total_contacts) * 100

print(f"Contact → Lead Conversion: {contact_to_lead:.2f}%")
print(f"Lead → Customer Conversion: {lead_to_customer:.2f}%")
print(f"Overall Conversion: {overall_conversion:.2f}%")

# ============================================
# 📉 6. DROP-OFF ANALYSIS
# ============================================

drop1 = ((total_contacts - leads) / total_contacts) * 100
drop2 = ((leads - customers) / leads) * 100

drop_df = pd.DataFrame({
    'Stage': ['Contact → Lead', 'Lead → Customer'],
    'Drop-off (%)': [drop1, drop2]
})

drop_df


# ============================================
# 📊 7. FUNNEL VISUALIZATION
# ============================================

plt.figure()
plt.bar(funnel['Stage'], funnel['Count'])
plt.title("Marketing Funnel")
plt.xlabel("Stage")
plt.ylabel("Number of People")
plt.show()

# ============================================
# 📊 8. DROP-OFF VISUALIZATION
# ============================================

plt.figure()
plt.bar(drop_df['Stage'], drop_df['Drop-off (%)'])
plt.title("Drop-off Percentage")
plt.xlabel("Stage")
plt.ylabel("Drop-off (%)")
plt.show()

# ============================================
# 📢 9. CHANNEL ANALYSIS (CONTACT TYPE)
# ============================================

channel = df.groupby('contact').agg({
    'y': ['count', 'sum']
})

channel.columns = ['Total Contacts', 'Customers']
channel['Conversion Rate (%)'] = (channel['Customers'] / channel['Total Contacts']) * 100

channel


# ============================================
# 📊 10. CHANNEL VISUALIZATION
# ============================================

plt.figure()
plt.bar(channel.index, channel['Conversion Rate (%)'])
plt.title("Conversion Rate by Contact Type")
plt.xlabel("Channel")
plt.ylabel("Conversion Rate (%)")
plt.show()

# ============================================
# 📅 11. TIME ANALYSIS (MONTH)
# ============================================

monthly = df.groupby('month')['y'].mean() * 100

plt.figure()
plt.bar(monthly.index, monthly.values)
plt.title("Conversion Rate by Month")
plt.xlabel("Month")
plt.ylabel("Conversion Rate (%)")
plt.xticks(rotation=45)
plt.show()


# ============================================
# 💡 12. FINAL INSIGHTS
# ============================================

print("\n📊 KEY INSIGHTS:")

if drop1 > drop2:
    print("- Major drop-off happens before lead generation")
else:
    print("- Major drop-off happens before final conversion")

print("- Improve targeting strategy if early funnel is weak")
print("- Optimize sales pitch if lead-to-customer conversion is low")
print("- Focus on best-performing contact channels")