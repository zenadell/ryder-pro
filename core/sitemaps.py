from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Vehicle, BlogPost, Job, InvestmentAsset

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'home', 'about', 'contact', 'faq', 'privacy', 'terms', 
            'all_cars', 'blog', 'jobs_list', 'invest_marketplace',
            'instructions', 'licenses'
        ]

    def location(self, item):
        return reverse(item)

class VehicleSitemap(Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return Vehicle.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('car_details', args=[obj.slug])

class BlogPostSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return BlogPost.objects.filter(is_published=True).order_by('-published_date')
        
    def lastmod(self, obj):
        return obj.published_date

    def location(self, obj):
        return reverse('blog_detail', args=[obj.slug])

class JobSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return Job.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('job_detail', args=[obj.id])

class InvestmentAssetSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return InvestmentAsset.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('invest_asset_detail', args=[obj.slug])

sitemaps = {
    'static': StaticViewSitemap,
    'vehicles': VehicleSitemap,
    'blog': BlogPostSitemap,
    'jobs': JobSitemap,
    'invest': InvestmentAssetSitemap,
}
