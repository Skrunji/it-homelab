import pandas as pd

df = pd.read_csv("csv-automation/device_inventory.csv")
filtered = df[df["status"].isin(["Unassigned", "Needs Repair"])]
report =  filtered[["asset_tag", "assigned_user", "room", "location"]].fillna("Unassigned")
report = report.sort_values(by=["location", "room"])

print("=== Device Inventory Report ===")
print("\nTotal Devices by Location:")
print(df.groupby("location")["asset_tag"].count().to_string())
print("\nDevices Needing Attention by Location:")
print(filtered.groupby("location")["asset_tag"].count().to_string())
print("\nDevices Needing Attention:")
print(report.to_string(index=False))


report.to_csv("csv-automation/devices_needing_attention.csv", index=False)