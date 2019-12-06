# coding: utf-8
from src.businesses.handlers.common.illegal_stats import IllegalStats

routes = [
    (r"/illegal/stats", IllegalStats, {}, "IllegalStats"),
]
