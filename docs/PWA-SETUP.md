# PWA Setup Guide for Ringette Game

Your Ringette game is now configured as a Progressive Web App (PWA)! 🎉

## ✅ What's Already Done

- ✅ **Web App Manifest** (`manifest.json`) - Defines app metadata
- ✅ **Service Worker** (`sw.js`) - Enables offline functionality
- ✅ **PWA Meta Tags** - Added to both `play.html` and `index.html`
- ✅ **Service Worker Registration** - Automatically registers when page loads
- ✅ **Install Prompt Handling** - Ready for "Add to Home Screen"

## 🎨 Create App Icons (Required)

You need to create PNG icons from the provided SVG template:

### Option 1: Online Converter (Easiest)

1. Go to https://convertio.co/svg-png/ or https://cloudconvert.com/svg-to-png
2. Upload `icon-template.svg`
3. Convert to PNG at these sizes:
   - **192x192** → Save as `icon-192.png`
   - **512x512** → Save as `icon-512.png`
4. Place both PNG files in the `docs/` folder

### Option 2: Using Inkscape (Free Desktop App)

```bash
# Install Inkscape (free vector graphics editor)
# Then export the SVG:
inkscape icon-template.svg --export-type=png --export-width=192 --export-filename=icon-192.png
inkscape icon-template.svg --export-type=png --export-width=512 --export-filename=icon-512.png
```

### Option 3: Using ImageMagick (Command Line)

```bash
# Install ImageMagick, then:
magick icon-template.svg -resize 192x192 icon-192.png
magick icon-template.svg -resize 512x512 icon-512.png
```

## 🧪 Testing Your PWA

### 1. Local Testing

```bash
# Serve from the docs folder using any local server:
cd docs
python -m http.server 8000
# Or: npx serve .
# Or: php -S localhost:8000
```

### 2. Check PWA Features

1. Open Chrome DevTools (F12)
2. Go to **Application** tab
3. Check **Manifest** section - should show your app details
4. Check **Service Workers** - should show registered worker
5. Try **Lighthouse** audit for PWA score

### 3. Test Installation

1. Visit your site on mobile Chrome/Safari
2. Look for "Add to Home Screen" prompt
3. On desktop Chrome: Look for install icon in address bar

## 🚀 Deployment Options

### GitHub Pages (Free & Easy)

```bash
# Push to GitHub, then enable Pages in repo settings
# Your PWA will be at: https://username.github.io/repository-name/
```

### Netlify (Free & Easy)

1. Drag your `docs` folder to https://netlify.com/
2. Instant HTTPS deployment
3. Auto-updates on Git commits

### Vercel (Free)

```bash
npm i -g vercel
cd docs
vercel --prod
```

## 📱 PWA Features Enabled

### ✅ Installable

- Can be installed on phone/desktop home screen
- Launches in fullscreen like a native app
- Custom app icon and splash screen

### ✅ Offline Capable

- Game works even without internet
- Files cached automatically
- Seamless online/offline switching

### ✅ Mobile Optimized

- Landscape orientation enforced on mobile
- Touch-friendly controls
- Native app-like feel

### ✅ Auto-Updates

- New versions download automatically
- Prompts user to refresh for updates
- Version-controlled caching

## 🔧 Customization

### Update App Info

Edit `manifest.json` to change:

- App name and description
- Theme colors
- Start URL
- Display mode

### Modify Caching

Edit `sw.js` to:

- Add more files to cache
- Change cache strategy
- Add offline fallback pages

### Add Features

- Push notifications
- Background sync
- Share target API
- File handling

## 🐛 Troubleshooting

### PWA Not Installing?

- Ensure HTTPS (required for PWA)
- Check manifest.json is valid
- Verify service worker registered
- Check browser compatibility

### Icons Not Showing?

- Make sure PNG files exist
- Check file paths in manifest.json
- Clear browser cache
- Verify icon sizes are correct

### Offline Not Working?

- Check service worker in DevTools
- Verify files are cached
- Test by disabling network in DevTools

## 📊 PWA Checklist

- ✅ Web App Manifest configured
- ✅ Service Worker registered
- ✅ HTTPS ready (when deployed)
- ⏳ Icons created (192px + 512px)
- ⏳ Deployed to HTTPS server
- ⏳ Tested installation flow
- ⏳ Verified offline functionality

Once you create the icons and deploy with HTTPS, your Ringette game will be a fully functional PWA! 🏒📱
