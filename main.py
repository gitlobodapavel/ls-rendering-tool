from api import services

from api.driver import Driver

if __name__ == '__main__':
    asset_ids = services.sku_to_id(services.parse_xlsx(filename='import.xlsx'))
    # asset_ids = ['ec3dfb0e-043e-4600-8dec-0e0c9058a7d1', ]

    driver = Driver()
    for asset_id in asset_ids:
        driver.get_page(asset_id)
        attributes = driver.get_attributes()

        materials = services.get_materials(attributes)
        layers = services.get_layers(attributes, services.get_composite(asset_id))

        # services.start_render_job(materials, layers, asset_id, services.get_stage_id(asset_id))