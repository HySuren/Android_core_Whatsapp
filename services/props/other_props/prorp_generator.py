from services.props.other_props.manager import PropModel


def gen_props_list(prop_model: PropModel) -> tuple[str, ...]:
  fingerprint_props = (
    f"ro.build.fingerprint={prop_model.fingerprint}",
    f"ro.odm.fingerprint={prop_model.fingerprint}",
    f"ro.odm.build.fingerprint={prop_model.fingerprint}",
    f"ro.bootimage.build.fingerprint={prop_model.fingerprint}",
    f"ro.product.fingerprint={prop_model.fingerprint}",
    f"ro.product.build.fingerprint={prop_model.fingerprint}",
    f"ro.system_ext.fingerprint={prop_model.fingerprint}",
    f"ro.system_ext.build.fingerprint={prop_model.fingerprint}",
    f"ro.system.fingerprint={prop_model.fingerprint}",
    f"ro.system.build.fingerprint={prop_model.fingerprint}",
    f"ro.vendor.fingerprint={prop_model.fingerprint}",
    f"ro.vendor.build.fingerprint={prop_model.fingerprint}",
  )
  brand_props = (
    f"ro.build.brand={prop_model.brand}",
    f"ro.odm.brand={prop_model.brand}",
    f"ro.product.odm.brand={prop_model.brand}",
    f"ro.product.brand={prop_model.brand}",
    f"ro.product.product.brand={prop_model.brand}",
    f"ro.system_ext.brand={prop_model.brand}",
    f"ro.product.system_ext.brand={prop_model.brand}",
    f"ro.system.brand={prop_model.brand}",
    f"ro.product.system.brand={prop_model.brand}",
    f"ro.vendor.brand={prop_model.brand}",
    f"ro.product.vendor.brand={prop_model.brand}",
  )
  manufacturer_props = (
    f"ro.build.manufacturer={prop_model.manufacturer}",
    f"ro.odm.manufacturer={prop_model.manufacturer}",
    f"ro.product.odm.manufacturer={prop_model.manufacturer}",
    f"ro.product.manufacturer={prop_model.manufacturer}",
    f"ro.product.product.manufacturer={prop_model.manufacturer}",
    f"ro.system_ext.manufacturer={prop_model.manufacturer}",
    f"ro.product.system_ext.manufacturer={prop_model.manufacturer}",
    f"ro.system.manufacturer={prop_model.manufacturer}",
    f"ro.product.system.manufacturer={prop_model.manufacturer}",
    f"ro.vendor.manufacturer={prop_model.manufacturer}",
    f"ro.product.vendor.manufacturer={prop_model.manufacturer}",
  )
  tags_props = (
    f"ro.build.tags={prop_model.tags}",
    f"ro.odm.tags={prop_model.tags}",
    f"ro.odm.build.tags={prop_model.tags}",
    f"ro.product.tags={prop_model.tags}",
    f"ro.product.build.tags={prop_model.tags}",
    f"ro.system_ext.tags={prop_model.tags}",
    f"ro.system_ext.build.tags={prop_model.tags}",
    f"ro.system.tags={prop_model.tags}",
    f"ro.system.build.tags={prop_model.tags}",
    f"ro.vendor.tags={prop_model.tags}",
    f"ro.vendor.build.tags={prop_model.tags}",
  )
  model_props = (
    f"ro.build.model={prop_model.model}",
    f"ro.odm.model={prop_model.model}",
    f"ro.product.odm.model={prop_model.model}",
    f"ro.product.model={prop_model.model}",
    f"ro.product.product.model={prop_model.model}",
    f"ro.system_ext.model={prop_model.model}",
    f"ro.product.system_ext.model={prop_model.model}",
    f"ro.system.model={prop_model.model}",
    f"ro.product.system.model={prop_model.model}",
    f"ro.vendor.model={prop_model.model}",
    f"ro.product.vendor.model={prop_model.model}",
  )
  name_props = (
    f"ro.build.name={prop_model.name}",
    f"ro.odm.name={prop_model.name}",
    f"ro.product.odm.name={prop_model.name}",
    f"ro.product.name={prop_model.name}",
    f"ro.product.product.name={prop_model.name}",
    f"ro.system_ext.name={prop_model.name}",
    f"ro.product.system_ext.name={prop_model.name}",
    f"ro.system.name={prop_model.name}",
    f"ro.product.system.name={prop_model.name}",
    f"ro.vendor.name={prop_model.name}",
    f"ro.product.vendor.name={prop_model.name}",
  )
  build_id_props = (
    f"ro.build.id={prop_model.build_id}",
    f"ro.odm.build../../../magiskid={prop_model.build_id}",
    f"ro.product.build../../../magiskid={prop_model.build_id}",
    f"ro.system_ext.build../../../magiskid={prop_model.build_id}",
    f"ro.system.build../../../magiskid={prop_model.build_id}",
    f"ro.vendor.build../../../magiskid={prop_model.build_id}",
    f"ro.omc.build.id={prop_model.build_id}",
  )
  device_props = (
    f"ro.build.device={prop_model.device}",
    f"ro.odm.device={prop_model.device}",
    f"ro.product.odm.device={prop_model.device}",
    f"ro.product.device={prop_model.device}",
    f"ro.product.product.device={prop_model.device}",
    f"ro.system_ext.device={prop_model.device}",
    f"ro.product.system_ext.device={prop_model.device}",
    f"ro.system.device={prop_model.device}",
    f"ro.product.system.device={prop_model.device}",
    f"ro.vendor.device={prop_model.device}",
    f"ro.product.vendor.device={prop_model.device}",
  )
  display_id_props = (
    f"ro.build.display../../../magiskid={prop_model.display_id}",
    f"ro.odm.display../../../magiskid={prop_model.display_id}",
    f"ro.product.display../../../magiskid={prop_model.display_id}",
    f"ro.system_ext.display../../../magiskid={prop_model.display_id}",
    f"ro.system.display../../../magiskid={prop_model.display_id}",
    f"ro.vendor.display../../../magiskid={prop_model.display_id}",
  )
  incremental_props = (
    f"ro.build.incremental={prop_model.incremental}",
    f"ro.build.version.incremental={prop_model.incremental}",
    f"ro.odm.incremental={prop_model.incremental}",
    f"ro.odm.build.version.incremental={prop_model.incremental}",
    f"ro.product.incremental={prop_model.incremental}",
    f"ro.product.build.version.incremental={prop_model.incremental}",
    f"ro.system_ext.incremental={prop_model.incremental}",
    f"ro.system_ext.build.version.incremental={prop_model.incremental}",
    f"ro.system.incremental={prop_model.incremental}",
    f"ro.system.build.version.incremental={prop_model.incremental}",
    f"ro.vendor.incremental={prop_model.incremental}",
    f"ro.vendor.build.version.incremental={prop_model.incremental}",
  )
  date_props = (
    f"ro.build.date={prop_model.date}",
    f"ro.odm.date={prop_model.date}",
    f"ro.odm.build.date={prop_model.date}",
    f"ro.bootimage.build.date={prop_model.date}",
    f"ro.product.date={prop_model.date}",
    f"ro.product.build.date={prop_model.date}",
    f"ro.system_ext.date={prop_model.date}",
    f"ro.system_ext.build.date={prop_model.date}",
    f"ro.system.date={prop_model.date}",
    f"ro.system.build.date={prop_model.date}",
    f"ro.vendor.date={prop_model.date}",
    f"ro.vendor.build.date={prop_model.date}",
    f"persist.sys.ccm.date={prop_model.date}",
    f"persist.sys.knoxvpn.date={prop_model.date}",
  )
  date_utc_props = (
    f"ro.build.date../../../magiskutc={prop_model.date_utc}",
    f"ro.odm.date../../../magiskutc={prop_model.date_utc}",
    f"ro.odm.build.date../../../magiskutc={prop_model.date_utc}",
    f"ro.bootimage.build.date../../../magiskutc={prop_model.date_utc}",
    f"ro.product.date../../../magiskutc={prop_model.date_utc}",
    f"ro.product.build.date../../../magiskutc={prop_model.date_utc}",
    f"ro.system_ext.date../../../magiskutc={prop_model.date_utc}",
    f"ro.system_ext.build.date../../../magiskutc={prop_model.date_utc}",
    f"ro.system.date../../../magiskutc={prop_model.date_utc}",
    f"ro.system.build.date../../../magiskutc={prop_model.date_utc}",
    f"ro.vendor.date../../../magiskutc={prop_model.date_utc}",
    f"ro.vendor.build.date../../../magiskutc={prop_model.date_utc}",
  )
  build_type_props = (
    f"ro.build.type={prop_model.build_type}",
    f"ro.odm.build../../../magisktype={prop_model.build_type}",
    f"ro.product.build../../../magisktype={prop_model.build_type}",
    f"ro.system_ext.build../../../magisktype={prop_model.build_type}",
    f"ro.system.build../../../magisktype={prop_model.build_type}",
    f"ro.vendor.build../../../magisktype={prop_model.build_type}",
  )
  build_user_props = (
    f"ro.build.user={prop_model.build_user}",
    f"ro.odm.build../../../magiskuser={prop_model.build_user}",
    f"ro.product.build../../../magiskuser={prop_model.build_user}",
    f"ro.system_ext.build../../../magiskuser={prop_model.build_user}",
    f"ro.system.build../../../magiskuser={prop_model.build_user}",
    f"ro.vendor.build../../../magiskuser={prop_model.build_user}",
  )
  host_props = (
    f"ro.build.host={prop_model.host}",
    f"ro.odm.host={prop_model.host}",
    f"ro.product.host={prop_model.host}",
    f"ro.system_ext.host={prop_model.host}",
    f"ro.system.host={prop_model.host}",
    f"ro.vendor.host={prop_model.host}",
  )
  flavor_props = (
    f"ro.build.flavor={prop_model.flavor}",
    f"ro.odm.flavor={prop_model.flavor}",
    f"ro.product.flavor={prop_model.flavor}",
    f"ro.system_ext.flavor={prop_model.flavor}",
    f"ro.system.flavor={prop_model.flavor}",
    f"ro.vendor.flavor={prop_model.flavor}",
  )

  return fingerprint_props \
    + brand_props \
    + manufacturer_props \
    + tags_props \
    + model_props \
    + name_props \
    + build_id_props \
    + device_props \
    + display_id_props \
    + incremental_props \
    + date_props \
    + date_utc_props \
    + build_type_props \
    + build_user_props \
    + host_props \
    + flavor_props
