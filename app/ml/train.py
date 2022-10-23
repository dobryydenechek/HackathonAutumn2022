from preprocess import read_pcap, preprocess_df, train_apps_model, train_classes_model

# df = read_pcap('testtest')
df = read_pcap('VPN-PCAPS-01')
done_df = preprocess_df(df)
classes_model = train_classes_model(done_df)
classes_model.save_model("saved_models/classes_model.txt")
# apps_model = train_apps_model(done_df)


# apps_model.save_model("saved_models/apps_model.txt")
