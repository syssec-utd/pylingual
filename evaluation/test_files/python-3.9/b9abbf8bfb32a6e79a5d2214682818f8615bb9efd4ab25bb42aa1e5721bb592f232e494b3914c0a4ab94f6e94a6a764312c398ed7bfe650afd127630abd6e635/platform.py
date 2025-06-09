import dataclasses
import typing
import dacite
import oci.client as oc
import oci.model as om

def from_manifest(image_reference: om.OciImageReference, manifest: om.OciImageManifest, oci_client: oc.Client=None, base_platform: om.OciPlatform=None) -> om.OciPlatform:
    if base_platform:
        cfg = base_platform.as_dict()
    else:
        cfg = {}
    cfg |= oci_client.blob(image_reference=image_reference, digest=manifest.config.digest, stream=False).json()
    return dacite.from_dict(data_class=om.OciPlatform, data=cfg)

def from_single_image(image_reference: typing.Union[str, om.OciImageReference], oci_client: oc.Client=None, base_platform: om.OciPlatform=None) -> om.OciPlatform:
    """
    determines the platform from a "single oci image" (i.e. an oci image which is _not_
    a multiarch image).
    """
    image_reference = om.OciImageReference.to_image_ref(image_reference)
    manifest = oci_client.manifest(image_reference=image_reference)
    if not isinstance(manifest, om.OciImageManifest):
        raise ValueError(f'image_reference={image_reference!r} did not yield OciImageManifest: type(manifest)={type(manifest)!r}')
    return from_manifest(manifest=manifest, oci_client=oci_client, base_platform=base_platform)

def single_platform_manifest(image_reference: om.OciImageReference | str, oci_client: oc.Client, platform: om.OciPlatform=None):
    """
    returns a single-platform OCI Image Manifest for the given image_reference.
    lookup and validation depend on presence of platform argument.

    if given image-ref points to a single-arch manifest, the returned result will be identical
    to invoking `oci_client.manifest`. If platform argument is passed, and the discovered
    platform does not match, a `ValueError` will be raised.

    if given image-ref points to a multi-arch manifest, content-negotiation depends on presence of
    platform-argument. If absent, no preference will be stated (i.e. accept-header will not be set).
    Some Oci-Image-registries will return a single-arch manifest (thus saving a roundtrip).
    If platform is passed, preference for multi-arch will be stated via accept-header; the specified
    platform will be looked-up and returned. If not found, `ValueError` will be raised.
    """
    image_reference = om.OciImageReference.to_image_ref(image_reference)
    if platform:
        accept = om.MimeTypes.prefer_multiarch
    else:
        accept = None
    manifest = oci_client.manifest(image_reference=image_reference, accept=accept)
    if isinstance(manifest, om.OciImageManifest):
        if not platform:
            return manifest
        actual_platform = from_manifest(manifest=manifest, oci_client=oci_client)
        if not actual_platform == platform:
            raise ValueError(f'image_reference={image_reference!r} does not match platform={platform!r}: actual_platform={actual_platform!r}')
        return manifest
    elif isinstance(manifest, om.OciImageManifestList):
        pass
    else:
        raise NotImplementedError(manifest)
    for manifest in manifest.manifests:
        manifest: om.OciImageManifestListEntry
        if manifest.platform == platform:
            break
    else:
        raise ValueError(f'image_reference={image_reference!r} does not contain platform={platform!r}')
    manifest_ref = f'{image_reference.ref_without_tag}@{manifest.digest}'
    return oci_client.manifest(image_reference=manifest_ref)

def iter_platforms(image_reference: typing.Union[str, om.OciImageReference], oci_client: oc.Client=None) -> typing.Generator[tuple[om.OciImageReference, om.OciPlatform], None, None]:
    image_reference = om.OciImageReference.to_image_ref(image_reference)
    manifest = oci_client.manifest(image_reference=image_reference, accept=om.MimeTypes.prefer_multiarch)
    if isinstance(manifest, om.OciImageManifest):
        platform = from_single_image(image_reference=image_reference, oci_client=oci_client)
        yield (image_reference, platform)
        return
    elif isinstance(manifest, om.OciImageManifestList):
        manifest: om.OciImageManifestList
    else:
        raise NotImplementedError(type(manifest))
    prefix = image_reference.ref_without_tag
    for sub_manifest in manifest.manifests:
        platform_dict = dataclasses.asdict(sub_manifest)
        sub_manifest = oci_client.manifest(image_reference=(sub_img_ref := f'{prefix}@{sub_manifest.digest}'))
        platform = from_single_image(image_reference=sub_img_ref, oci_client=oci_client)
        platform_dict |= dataclasses.asdict(platform)
        platform = dacite.from_dict(data_class=om.OciPlatform, data=platform_dict)
        yield (sub_img_ref, platform)