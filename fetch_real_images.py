import os
import requests

os.makedirs('media/invest', exist_ok=True)

categories = {
    'truck': 'https://loremflickr.com/800/600/semi-truck',
    'bus': 'https://loremflickr.com/800/600/coach-bus',
    'van': 'https://loremflickr.com/800/600/cargo-van',
    'tractor': 'https://loremflickr.com/800/600/tractor,farm',
    'motorcycle': 'https://loremflickr.com/800/600/motorcycle,sport',
    'car': 'https://loremflickr.com/800/600/sedan,car'
}

def main():
    for category, url in categories.items():
        print(f"Downloading {category}...")
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                with open(f'media/invest/{category}.jpg', 'wb') as f:
                    f.write(r.content)
                print(f"Successfully saved {category}.jpg")
            else:
                print(f"Failed to download {category}: HTTP {r.status_code}")
        except Exception as e:
            print(f"Error downloading {category}: {e}")

if __name__ == '__main__':
    main()
