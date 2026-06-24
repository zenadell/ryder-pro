import google from 'googlethis';

async function fetchImage() {
    const args = process.argv.slice(2);
    const query = args[0];

    if (!query) {
        console.log('NONE');
        return;
    }

    try {
        const images = await google.image(query, { safe: false });
        if (images && images.length > 0) {
            let bestImage = null;
            let maxRes = 0;
            
            for (let img of images) {
                if (img.url.includes('thumb') || img.url.includes('icon') || img.url.includes('logo')) continue;
                if (img.width > img.height && img.width >= 800) {
                    let res = img.width * img.height;
                    if (res > maxRes) {
                        maxRes = res;
                        bestImage = img.url;
                    }
                }
            }
            if (bestImage) {
                console.log(bestImage);
            } else {
                console.log(images[0].url);
            }
        } else {
            console.log('NONE');
        }
    } catch (e) {
        console.log('NONE');
    }
}
fetchImage();
