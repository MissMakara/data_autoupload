
1. Get business_id
SELECT business_id from business where business_account = billing_account;

2. Get reference_no
SELECT count(reference_number) from products
where business_id = business_id;

reference_number = count+1

3. add product_name, product_code, cost, price,

4. add allow_purchase, allow_sale, notes, track_inventory,notes(can be null)

5. get vendor_id
SELECT vendor_id FROM vendor WHERE vendor_name=vendor_name and business_id=business_id

6. get uom_id
SELECT uom_id FROM uom WHERE uom_name = uom_name and business_id =business_id

7. get expense_group
SELECT expense_group_id FROM expense_group WHERE group_name= expense_group_name and business_id=business_id

8. get tax_class_id
SELECT tax_class_id FROM tax_class WHERE class_name=tax_class_name and business_id=business_id

9. get product_group_id
SELECT product_group_id FROM product_group WHERE group_name=product_group_name and business_id=business_id

billing_account ,tax_class_name, alert_quantity, product_type, product_nature,earn_commission,media_id, commission_type_id - not given

