import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'backend'))

print(f"Path: {sys.path}")

try:
    print("Attempting to import playwright...")
    import playwright
    print("Playwright imported.")
except ImportError as e:
    print(f"Failed to import playwright: {e}")

try:
    print("Attempting to import backend.crawlers.nasa...")
    from backend.crawlers import nasa
    print("Import backend.crawlers.nasa success")
except Exception as e:
    print(f"backend.crawlers.nasa failed: {e}")

try:
    print("Attempting to import crawlers.nasa (if running from backend dir logic)...")
    from crawlers import nasa
    print("Import crawlers.nasa success")
except Exception as e:
    print(f"crawlers.nasa failed: {e}")

try:
    print("Attempting to import backend.crawlers.meta...")
    from backend.crawlers import meta
    print("Import backend.crawlers.meta success")
except Exception as e:
    print(f"backend.crawlers.meta failed: {e}")

try:
    print("Attempting to import backend.crawlers.apple...")
    from backend.crawlers import apple
    print("✅ backend.crawlers.apple imported successfully")
except ImportError as e:
    print(f"❌ Failed to import backend.crawlers.apple: {e}")

try:
    print("Attempting to import backend.crawlers.goldman_sachs...")
    from backend.crawlers import goldman_sachs
    print("✅ backend.crawlers.goldman_sachs imported successfully")
except ImportError as e:
    print(f"❌ Failed to import backend.crawlers.goldman_sachs: {e}")
