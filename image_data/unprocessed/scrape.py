from bing_image_downloader import downloader

# Download images of fish with fin rot
downloader.download("fish with fin rot in aquarium zoomed in real", limit=250,  output_dir='fin_rot', adult_filter_off=True, force_replace=False, timeout=60)


