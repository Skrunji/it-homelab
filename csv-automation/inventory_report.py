import pandas as pd

df = pd.read_csv("csv-automation/device_inventory.csv")

print("=== Device Inventory Report ===")
print("\nTotal Devices by Location:")
print(df.groupby("location")["asset_tag"].count())

filtered = df[df["status"].isin(["Unassigned", "Needs Repair"])]


print("\nDevices Needing Attention:")
print(filtered[["asset_tag", "assigned_user", "room", "location"]].fillna("Unassigned"))

filtered[["asset_tag", "assigned_user", "room", "location"]].fillna("Unassigned").to_csv("csv-automation/devices_needing_attention.csv", index=False)